from django.contrib import admin
from mainapp.models import News, Course, Lesson, CourseTeachers


admin.site.register(News)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseTeachers)
