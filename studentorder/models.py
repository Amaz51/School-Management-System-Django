from django.db import models
from students.models import Student 
from django.conf import settings
class StudentOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'student')
        ordering = ['order']
        db_table = 'student_order'

    def __str__(self):
        return f"{self.user.username} - {self.student.name} ({self.order})"
