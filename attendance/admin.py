from django.contrib import admin
from .models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display=['student','date','status','class_obj__name', 'Courses']
    search_fields=['student','status','class_obj__name']
    list_filter = ['student__name', 'student__student_id','class_obj__name']
    def Courses(self, obj):
        if obj.class_obj and hasattr(obj.class_obj, 'courses'):
            return ", ".join(course.name for course in obj.class_obj.courses.all())
        return "No Courses"
    
admin.site.register(Attendance,AttendanceAdmin)
