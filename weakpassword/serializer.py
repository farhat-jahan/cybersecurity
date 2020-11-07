from rest_framework import serializers, fields
from . models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):

    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model  = UserProfile
        #fields =  '__all__'
      #  exclude = ['created_date']
        fields = ['user','date_of_birth','contact_number', 'address']

    # def get_username(self):
    #     print("oo?????????????????")
    #     userprofile = UserProfile.objects.select_related('user').all()
    #     print("oo?????????????????", userprofile)
    #     username = userprofile.user
    #     print("username=================", username)
    #     return username
#
# class UserSerializer(serializers.ModelSerializer):
#     userprofile_user = UserProfileSerializer(required=True, many=True)
#     class Meta:
#         model  = User
#         fields =  ['username', 'first_name','last_name', 'userprofile_user']
#
#     def create(self, validated_data):
#         userprofile_data = validated_data.pop('userprofile_user')
#         userprofile = User.objects.create(**validated_data)
#
#         UserProfile.objects.create(user=userprofile, **userprofile_data)
#         return userprofile

class UserProfileUpdateSerializer(serializers.ModelSerializer):

  #  username  = serializers.SerializerMethodField('get_username')
    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model  = UserProfile
        fields =  '__all__'
      #  exclude = ['created_date']
       # fields = ['username', 'date_of_birth','contact_number', 'address']

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        depth = 1

    # def to_representation(self, instance):
    #     return "your way of representation"
