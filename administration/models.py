from django.db import models
from user.models import User

class Administration(models.Model):
    name = models.CharField(max_length = 50)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name