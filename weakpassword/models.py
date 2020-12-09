from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser
import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_jwt.settings import api_settings

class UserProfile(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    contact_number = models.IntegerField()
    second_contact_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length= 50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length= 4)

    class Meta:
        db_table = "userprofile"

    def __str__(self):
        return self.user.first_name

# class JwtUserProfile(models.Model):
#     created_date = models.DateTimeField(auto_now_add=True)
#     id = models.AutoField(primary_key=True, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
#
#     contact_number = models.IntegerField()
#     second_contact_number = models.IntegerField(blank=True, null=True)
#     address = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     gender = models.CharField(max_length=4)
#
#     class Meta:
#         db_table = "jwt_userprofile"
#
#     def __str__(self):
#         return self.user.first_name

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def generate_jwt_token_for_users(sender, instance=None, created=False):
#     """
#     JWT token get created for all registered users.
#     :param sender:
#     :param instance:
#     :param created:
#     :return:
#     """
#     if created:






