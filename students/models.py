from django.db import models
from django.conf import settings
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    order=models.PositiveIntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table='student'
        ordering = ['order']

    def __str__(self):
        return f"{self.student_id} - {self.name} - {self.email}"