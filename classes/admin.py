from django.contrib import admin
from .models import Class
from attendance.models import Attendance
from courses.models import Course
# Register your models here.

class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 1

class CourseInline(admin.StackedInline):
    model=Course
    extra=1


class ClassAdmin(admin.ModelAdmin):
    list_display=['name']
    search_fields=['name']
    list_filter=['name']
    inlines=[AttendanceInline,CourseInline]

admin.site.register(Class,ClassAdmin)
