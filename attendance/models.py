from django.db import models
from students.models import Student
from classes.models import Class
# class Attendance(models.Model):
#     class Status(models.TextChoices):
#         PRESENT = 'Present', 'Present'
#         ABSENT = 'Absent', 'Absent'

#     student=models.ForeignKey(Student,on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=10, choices=Status.choices)

#     class Meta:
#         db_table='attendance'
#     def __str__(self):
#         return f"{self.student.name} - {self.date} - {self.status}"

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'Present', 'Present'
        ABSENT = 'Absent', 'Absent'

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)

    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)

    class Meta:
        db_table = 'attendance'

    
    def __str__(self):
        student_name = self.student.name if self.student else "Unknown Student"
        class_name = self.class_obj.name if self.class_obj else "Unknown Class"
        return f"{student_name} - {class_name} - {self.date} - {self.status}"
