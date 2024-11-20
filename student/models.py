from django.db import models
from classroom.models import Classroom
from user.models import User

class Student(models.Model):
    s_name = models.CharField(max_length = 50)
    grade = models.CharField(max_length = 10)
    class_enrolled = models.ForeignKey(Classroom, on_delete=models.CASCADE, null= True, blank = True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null= True, blank =True)
    image = models.ImageField(upload_to='images/',null=True, blank = True)

    def __str__(self):
        return self.s_name