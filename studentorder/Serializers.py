from rest_framework import serializers
from .models import StudentOrder
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email']

class StudentOrderSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = StudentOrder
        fields = ['student', 'order']
