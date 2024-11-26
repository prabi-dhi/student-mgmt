from django.db import models
from classroom.models import Classroom
# from subject.models import Subject
from user.models import User

class Teacher(models.Model):
    name = models.CharField(max_length = 50)
    department = models.CharField(max_length = 50)
    # department = models.ForeignKey(Subject, on_delete= models.CASCADE, null = True, blank = True)
    class_assigned = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank = True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null =True, blank = True)
    image = models.ImageField(upload_to='images/teachers',blank = True)

    class Meta:
        db_table = 'TEACHER'
        
    def __str__(self):
        return self.name
    