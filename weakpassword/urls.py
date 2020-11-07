from django.urls import path, re_path
from .views import add_user, get_users,update_user, delete_user, generate_jwt,adduser_using_jwt, test_add_user

app_name = 'weakpassword'

urlpatterns = [
        #These URL is used for CRUD operations without authenticating the API's requested users
        path('adduser/', add_user, name='add_user'),
        path('getusers/', get_users, name='get_users'),
        re_path('updateuser/(?:user-(?P<user_id>\d+)/)$', update_user, name='update_user'),
        re_path('deleteuser/(?:user-(?P<user_id>\d+)/)$', delete_user, name='delete_user'),
      #  path('updateuser/<user_id>/', update_user, name='update_user'),

        path('getjwt/', generate_jwt, name='generate_jwt'),

        #These URL is used for GET & POST data after authenticating the Api's requested users
        path('usingjwt/adduser/', adduser_using_jwt, name='adduser_using_jwt'),
       # path('usingjwt/getusers/', getusers_using_jwt, name='getusers_using_jwt'),

      #  path('testadduser/', test_add_user, name='test_add_user'),

]