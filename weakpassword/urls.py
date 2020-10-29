from django.urls import path
from .views import index, registration


urlpatterns = [
    path('', index, name='index'),
        #This URL is used for GET & POST data without authenticating the request.user
        path('registration/', registration, name='registration'),

]