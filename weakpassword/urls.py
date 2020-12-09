from django.urls import path, re_path
from .views import add_user, get_users,update_user, delete_user, get_jwt,adduser_using_jwt, getusers_using_jwt,\
        user_registration, index

app_name = 'weakpassword'

urlpatterns = [
        #These URL is used for CRUD operations without authenticating the API's requested users
        path('apis/adduser/', add_user, name='add_user'),
        path('apis/getusers/', get_users, name='get_users'),
        re_path('apis/updateuser/(?:user-(?P<user_id>\d+)/)$', update_user, name='update_user'),
        re_path('apis/deleteuser/(?:user-(?P<user_id>\d+)/)$', delete_user, name='delete_user'),

        path('apis/getjwt/', get_jwt, name='get_jwt'),

        #These URL is used for GET & POST data after authenticating the Api's requested users
        path('apis/usingjwt/adduser/', adduser_using_jwt, name='adduser_using_jwt'),
        path('apis/usingjwt/getusers/', getusers_using_jwt, name='getusers_using_jwt'),

        #These URL is used for UI side
       # path('ui/index/', index, name='index'),
       # path('ui/registration/', user_registration, name='user_registration'),


]