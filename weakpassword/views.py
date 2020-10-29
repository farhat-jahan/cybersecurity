from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from .serializer import UserProfileSerializer
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

@api_view(['POST', 'GET'])
def registration(request):
    """
    This function creates users and return users
    :param request:
    :return:
    """

    if request.method == 'GET':
        user_details = UserProfile.objects.all()
        serilizer_data = UserProfileSerializer(user_details, many=True)
        return JSONResponse(serilizer_data.data)

    elif request.method == 'POST':
        try:
            # UserProfile.objects.all().delete()# use to truncate this table
            # return Response('Data is truncated')

            check_user = User.objects.get(username=request.data['username'])
            check_user.check_password(request.data['password'])

            return Response({'User already exiting':request.data['username']+ ' and ' +request.data['password']}\
                            , status=status.HTTP_400_BAD_REQUEST)
        except:
            create_user = User(username=request.data['username'])
            create_user.set_password(request.data['password'])
            create_user.save()

            create_user.first_name = request.data['first_name']
            create_user.last_name = request.data['last_name']
            create_user.save()

        user_serailizer = UserProfileSerializer(data= {'contact_number':request.data['contact_number']\
                                                   ,'date_of_birth':request.data['date_of_birth'],'gender':request.data['gender'] \
                                          ,'user':create_user.id,'address':request.data['address']})
        if user_serailizer.is_valid():
            user_serailizer.save()
            return Response((user_serailizer.data), status=status.HTTP_200_OK)

        return Response(user_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

        #     return JSONResponse((user_serailizer.data), status=status.HTTP_200_OK)
        # return JSONResponse( user_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)





