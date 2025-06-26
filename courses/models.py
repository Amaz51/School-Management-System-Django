from django.db import models
from classes.models import Class
# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20,unique=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        db_table = 'course'

    def __str__(self):
        return f"{self.name} ({self.code})"
