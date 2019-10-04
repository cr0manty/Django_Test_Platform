

from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_page, name='home_url'),
    path('login/', LoginUser.as_view(), name='login_url'),
    path('registration/', RegisterUser.as_view(), name='registration_url'),
    path('logout/', LogoutUser.as_view(), name='logout_url'),
    path('user/<username>/', show_user, name='user_url'),
    path('user/', redirect_to_user),
]
