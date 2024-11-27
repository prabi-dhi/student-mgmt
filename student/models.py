from django.db import models
from classroom.models import Classroom
from user.models import User
from subject.models import Subject

class Student(models.Model):
    s_name = models.CharField(max_length = 50)
    grade = models.CharField(max_length = 10)
    class_enrolled = models.ForeignKey(Classroom, on_delete=models.CASCADE, null= True, blank = True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null= True, blank =True)
    image = models.ImageField(upload_to='images/students',null=True, blank = True)
    subjects = models.ManyToManyField(Subject)
    class Meta:
        db_table = 'STUDENT'
    def __str__(self):
        return self.s_name