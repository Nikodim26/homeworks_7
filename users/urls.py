from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import PaymentViewSet, UserCreateView, email_verification, IntermediateView, UserProfileAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='users:login', permanent=False), name='root'),
    path('login/', LoginView.as_view(template_name='login_register.html', form_class=UserLoginForm), name='login'),
    path('login_/', IntermediateView.as_view(), name='login_'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("api/profile/", UserProfileAPIView.as_view(), name="profile"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/', include(router.urls)),

] + router.urls


