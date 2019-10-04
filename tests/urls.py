from django.urls import path
from .views import *

urlpatterns = [
    path('', show_tests, name='test_list'),
    path('create/', CreateTest.as_view(), name='create_test'),
    path('<slug>/', ShowTest.as_view(), name='test_show'),
    path('<str:slug>/start', ShowTest.as_view(), name='start_test'),
    path('<str:slug>/result', ShowTest.as_view(), name='test_result'),
    path('<str:slug>/add_comment', AddComment.as_view(), name='add_comment_url'),
]
