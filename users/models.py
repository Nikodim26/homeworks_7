from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/image', verbose_name='Аватар', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='Телефон',blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна',blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['id']


    def __str__(self):
        return self.email


class Payment(models.Model):

    PAYMENT_METHODS = [('наличные', 'Наличные'), ('перевод на счет', 'Перевод на счет'), ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='покупатель', related_name='payments', )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты', )
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='оплаченный курс', related_name='payments', )
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='оплаченный урок', related_name='payments', )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты', )
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='перевод на счет',
                                      verbose_name='способ оплаты', )

    def __str__(self):
        return f'{self.user}: {self.paid_course or self.paid_lesson} — {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['payment_date']

    def save(self, *args, **kwargs):
        if self.paid_lesson and not self.paid_course:
            self.paid_course = self.paid_lesson.course
        super().save(*args, **kwargs)