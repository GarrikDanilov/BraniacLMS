from django.contrib import admin
from mainapp.models import News, Course, Lesson, CourseTeachers, CourseFeedback


admin.site.register(Course)
admin.site.register(CourseTeachers)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "title",
        "preamble",
        "created",
        "updated",
        "deleted"
    ]
    list_per_page = 5
    list_filter = ["deleted", "created"]
    search_fields = ["title", "preamble", "body"]
    actions = ["mark_as_deleted"]

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = "Пометить удаленным"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "get_course_name",
        "num", 
        "title",
        "created",
        "updated",
        "deleted"
        ]
    list_per_page = 4 
    ordering = ["course__name", "num"]
    list_filter = ["course", "created", "deleted"]
    actions = ["mark_as_deleted"]

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = "Пометить удаленным"

    def get_course_name(self, obj):
        return obj.course.name
    
    get_course_name.short_description = "Курс"


@admin.register(CourseFeedback)
class CourseFeedbackAdmin(admin.ModelAdmin):
    list_display = ["pk", "get_course_name", "get_username", "created"]

    def get_course_name(self, obj):
        return obj.course.name
    
    get_course_name.short_description = "Курс"

    def get_username(self, obj):
        return obj.user.username
    
    get_username.short_description = "Пользователь"
