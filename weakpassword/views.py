from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate
import datetime

from .serializer import UserProfileSerializer, UserUpdateSerializer, \
    UserAndUserProfileSerializer
from . models import UserProfile

#TODO : JSONResponse is not used
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
    """
    This function is used to display website index-page
    :param request:
    :return:
    """
    return render(request, 'weakpassword/index.html')


@api_view(['POST'])
@permission_classes((AllowAny,))
def add_user(request):
    """
    Creates new users and return all users details, any user can access this function, no authentication required
    :param request:
    :return:
    """
    try:
        check_user = User.objects.get(username=request.data['username'])
        # check_user.check_password(request.data['password'])
        return Response({'Error': 'Username: ' + request.data['username'] + ' is already existed'} \
                        , status=status.HTTP_400_BAD_REQUEST)
    except:
        create_user = User(username=request.data['username'])
        create_user.set_password(request.data['password'])
        create_user.save()
        create_user.first_name = request.data['first_name']
        create_user.last_name = request.data['last_name']
        create_user.save()


    user_serailizer = UserProfileSerializer(data= {'contact_number':request.data['contact_number']\
                                                   ,'date_of_birth':request.data['date_of_birth'],
                                                   'gender':request.data['gender'] \
                                          ,'user':create_user.id,'address':request.data['address']})
    if user_serailizer.is_valid():
        user_serailizer.save()
        response_data = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'User added successfully',
                'user data': request.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    return Response(user_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_users(request):
    """
    returns all the users and details. without authenticating the requested user.
    :param request: None
    :return: registered/ all Users
    """
    user_details = UserProfile.objects.all().select_related('user')
    serilizer_data = UserAndUserProfileSerializer(user_details, many=True)
    return JSONResponse(serilizer_data.data)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_user(request, user_id):
    """
    Updates the requested user.
    :param request:
    :param arg: user id # this is User model's id
    :return:
    """
    try:
        user_id = int(user_id)
        check_user =  User.objects.get(id=user_id)#.prefetch_related('')
        check_user_serealizer = UserUpdateSerializer(check_user, data=request.data)

        if check_user_serealizer.is_valid():
            check_user_serealizer.update(check_user, request.data)
            return Response(check_user_serealizer.data, status=status.HTTP_200_OK)

        return Response(check_user_serealizer.errors,status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({'Error': 'requested users id does not exist', 'status': status.HTTP_404_NOT_FOUND})


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_user(request, user_id):
    """
        Deletes the requested user.
        :param request:
        :param arg: user id # this is User model's id
        :return:
        """

    try:
        user_id = int(user_id)
        check_user = User.objects.get(id=user_id)
    except:
        return Response({'Error': 'requested users id does not exist', 'status': status.HTTP_404_NOT_FOUND})

    try:
        userprofile = UserProfile.objects.get(user=user_id)
    except :
        return Response({'Error':'Userprofile does not existed'}, status=status.HTTP_200_OK)

    check_user.delete()
    userprofile.delete()
    response_data = {
        'success': 'True',
        'status code': status.HTTP_200_OK,
        'message': 'User deleted successfully',
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def generate_jwt(request):

    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is None:
        return Response({'Error': 'Could not authenticate username & password'}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_jwt = create_jwt(user)
        response_data = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'Token created for registered user:'+request.data['username'],
            'user token': user_jwt
        }
        return Response(response_data, status=status.HTTP_200_OK)


def create_jwt(user):

    api_settings.JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=30000)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    jwt_token = jwt_encode_handler(payload)

    return jwt_token

@api_view(['POST'])
@permission_classes
def adduser_using_jwt(request):
    """
        Creates users and returns users: 'after authenticating the JWT'
        :param request:
        :return:
        """
    try:
        check_user = User.objects.get(username=request.data['username'])
        check_user.check_password(request.data['password'])
        return Response({'Error': 'Username:' + request.data['username'] +' already existed'} \
                            , status=status.HTTP_400_BAD_REQUEST)

            # check_user = authenticate(username=request.data['username'], password=request.data['password'])
            # if check_user is None:
            #     return Response({"duplicate data": "False"})
            # else:
            #     return Response({'User already exited':request.data['username']+ ' and ' +request.data['password']}\
            #                 , status=status.HTTP_400_BAD_REQUEST)

    except:
        create_user = User(username=request.data['username'])
        create_user.set_password(request.data['password'])
        create_user.save()

        create_user.first_name = request.data['first_name']
        create_user.last_name = request.data['last_name']
        create_user.save()

        user_serailizer = UserProfileSerializer(data={'contact_number': request.data['contact_number'] \
            , 'date_of_birth': request.data['date_of_birth'], 'gender': request.data['gender'] \
            , 'user': create_user.id, 'address': request.data['address']})
    if user_serailizer.is_valid():
        user_serailizer.save()
        response_data = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'User added successfully',
                'user data': user_serailizer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    return Response(user_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getusers_using_jwt():

    print("here inside=================")
    user_details = UserProfile.objects.all()
    serilizer_data = UserProfileSerializer(user_details, many=True)
    return JSONResponse(serilizer_data.data)




