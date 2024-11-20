from django.db import models
from teacher.models import Teacher

class Subject(models.Model):
    sub_code = models.CharField(max_length=10)
    sub_name = models.CharField(max_length = 50)
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.sub_name