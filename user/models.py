from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        ADMINISTRATION = "ADMINISTRATION", "Administration"

    user_type = models.CharField(max_length=20, choices=Types.choices, default=Types.STUDENT)
    # password = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=50)
    # image = models.ImageField(upload_to='images/',blank = True, null=True)
    username = models.CharField(unique=True, max_length=40)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]  

    class Meta:
        db_table = "USER"

    def __str__(self):
        return self.username
    

