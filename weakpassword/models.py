from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
   # modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    second_contact_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length= 50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length= 4)

    class Meta:
        db_table = "cyber_userprofile"




