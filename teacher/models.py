from django.db import models
from classroom.models import Classroom
from user.models import User

class Teacher(models.Model):
    name = models.CharField(max_length = 50)
    department = models.CharField(max_length = 50)
    class_assigned = models.OneToOneField(Classroom, on_delete=models.CASCADE, null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='images/',blank = True)

    def __str__(self):
        return self.name
    