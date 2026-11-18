from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса')
    image = models.ImageField(upload_to='materials/image', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тема урока')
    image = models.ImageField(upload_to='materials/image', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    video_link = models.URLField(max_length=500, blank=True, null=True, verbose_name='Ссылка на видео урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']
