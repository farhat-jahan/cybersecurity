from rest_framework import serializers, fields
from . models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):

    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    print(date_of_birth)
    class Meta:
        model  = UserProfile
        #fields =  '__all__'
        exclude = ['created_date']
