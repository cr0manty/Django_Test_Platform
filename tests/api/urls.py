from django.urls import path
from .views import *

all_tests = AllTestsViewSet.as_view({'get': "list"})

urlpatterns = [
    path('', all_tests, name='show_all_test'),
]
