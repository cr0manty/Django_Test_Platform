from django.urls import path
from .views import *

urlpatterns = [
    path('', show_tests, name='test_list'),
    path('create/', CreateTest.as_view(), name='create_test'),
    path('filter/', show_filter_tests, name='filter_tests'),
    path('<slug>/', ShowTest.as_view(), name='test_show'),
    path('<str:slug>/start', PassTest.as_view(), name='start_test'),
    path('<str:slug>/result', show_result, name='test_result'),
    path('<str:slug>/add_comment', AddComment.as_view(), name='add_comment_url'),
]
