from .models import Attendance
from rest_framework import serializers

from students.models import Student
from students.serializers import StudentSerializer
# class AttendanceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Attendance
#         fields = ['id', 'studentname', 'date', 'status']


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_id', 'date', 'status']
