from django.db import models
from students.models import Student
# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=20)
    students = models.ManyToManyField(Student, related_name='classes')

    class Meta:
        db_table = 'class'

    def __str__(self):
        return self.name
