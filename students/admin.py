from django.contrib import admin
from .models import Student
from attendance.models import Attendance
# Register your models here.
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'email'] #to display in list view
    search_fields = ['name', 'student_id']#field to include in search bar
    list_filter = ['email']   # field to filter in sidebar
    inlines = [AttendanceInline]


admin.site.register(Student,StudentAdmin)
