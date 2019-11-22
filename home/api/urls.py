from django.urls import path
from .views import *

all_user = AllUsersViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})
user_info = AllUsersViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', all_user, name='api_user_list'),
    path('<username>/', UserInfoAPI.as_view(), name='api_user_info'),
    path('<username>/comments/', UserCommentsAPI.as_view(), name='api_user_comments'),
    path('<username>/comments/<id>', UserCommentAPI.as_view(), name='api_user_comment'),
    path('<username>/tests/created/', UserTestsCreateAPI.as_view(), name='api_user_tests_created'),
    path('<username>/tests/pass/', UserTestsPassAPI.as_view(), name='api_user_tests_pass'),
]
