from django.contrib import admin

from materials.models import Course, Lesson
from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone_number','country')
    search_fields = ('email','phone_number','country')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','payment_date','paid_lesson','amount')
    search_fields = ('amount',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','name','description')
    search_fields = ('name','description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')