import secrets

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from config import settings
from users.filters import PaymentFilter
from users.forms import UserRegisterForm
from users.models import Payment, User
from users.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'login_register.html'
    success_url = reverse_lazy("users:login_")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        url = self.request.build_absolute_uri(
            reverse('users:email-confirm', kwargs={'token': token})
        )

        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке, чтобы подтвердить почту: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        self.object = user
        return HttpResponseRedirect(self.get_success_url())


def email_verification(request, token):
    user = get_object_or_404(User, token=token)

    user.is_active = True
    user.token = ''
    user.save()

    return redirect(reverse('users:login'))

class IntermediateView(TemplateView):
    template_name = 'intermediate.html'