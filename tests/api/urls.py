from django.urls import path
from .views import *

all_tests = AllTestsViewSet.as_view({'get': "list"})
all_results = AllTestsResultViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', all_tests, name='api_all_tests'),
    path('result/', all_results, name='api_all_results'),

]
