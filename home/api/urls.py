from django.urls import path
from .views import *

all_user = AllUsersViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', all_user, name='api_user_list'),
    path('<username>/', UserInfoAPI.as_view(), name='api_user_info'),
    path('<username>/comments/', UserCommentsAPI.as_view(), name='api_user_comments'),
    path('<username>/tests/', UserTestsAPI.as_view(), name='api_user_tests')

]
