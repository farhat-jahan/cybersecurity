from rest_framework import serializers, fields
from . models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model  = UserProfile
        fields = ['user','date_of_birth','contact_number', 'address']

class UserAndUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_username_from_user')

    class Meta:
        model = UserProfile
        fields = ['date_of_birth','contact_number', 'address', 'user']

    def get_username_from_user(self, userprofile_obj):
        user_data = { 'first_name':userprofile_obj.user.first_name, 'last_name': userprofile_obj.user.username}
        return user_data


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
#

class UserUpdateSerializer(serializers.ModelSerializer):
    userprofile =  serializers.SerializerMethodField('get_userprofile')

    class Meta:
        model = User
        fields = ['userprofile','id', 'first_name', 'last_name']
        read_only = id
      #  depth = 1

    def update(self, userobj, validated_data):
        if userobj:
            userobj.first_name = validated_data['first_name']
            userobj.last_name = validated_data['last_name']
            userobj.save()
        try:
            user_profile = UserProfile.objects.get(user__id=userobj.id)
            user_profile.contact_number = validated_data['contact_number']
            user_profile.save()
        except Exception as e:
            return {'Error':'Userprofile is missing'}

        return userobj

    def get_userprofile(self, userobj):

        userprofile = UserProfile.objects.get(user__id=userobj.id)
        if userprofile:
            userprofile_data = {'contact':userprofile.contact_number, 'address':userprofile.address,
                            'date_of_birth':userprofile.date_of_birth,'pk':userprofile.id,}

            return userprofile_data
        return {'Userprofile': None}

class UserProfileJWTSerializer(serializers.ModelSerializer):
    date_of_birth = fields.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model  = UserProfile
        fields = ['user','date_of_birth','contact_number', 'address']



