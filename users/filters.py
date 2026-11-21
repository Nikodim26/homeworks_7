import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(field_name='paid_course', label='ID курса')
    paid_lesson = django_filters.NumberFilter(field_name='paid_lesson', label='ID урока')
    payment_method = django_filters.CharFilter(field_name='payment_method', lookup_expr='exact')
    payment_date = django_filters.OrderingFilter(
        fields=('payment_date',),
        label='Сортировка по дате оплаты',
    )

    class Meta:
        model = Payment
        fields = ['paid_course', 'paid_lesson', 'payment_method']
