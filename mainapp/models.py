from django.db import models


class News(models.Model):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    preamble = models.CharField(max_length=1024, verbose_name="Вступление")

    body = models.TextField(blank=True, null=True, verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Разметка в формате Markdown")

    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создана")
    updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Обновлена")
    deleted = models.BooleanField(default=False, verbose_name="Удалена")

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'    


class Course(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Стоимость")

    description_as_markdown = models.BooleanField(default=False, verbose_name="Разметка в формате Markdown")
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Обложка")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'     


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    num = models.PositiveIntegerField(verbose_name="Номер урока")
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    description_as_markdown = models.BooleanField(default=False, verbose_name="Разметка в формате Markdown")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        ordering = ("course", "num")
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeachers(models.Model):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=256, verbose_name="Имя")
    name_second = models.CharField(max_length=256, verbose_name="Фамилия")
    day_birth = models.DateField(verbose_name="Дата рождения")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'     
