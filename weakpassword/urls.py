from django.urls import path
from .views import registration


urlpatterns = [
        #This URL is used for GET & POST data without authenticating the request.user
        path('registration/', registration, name='registration'),

]