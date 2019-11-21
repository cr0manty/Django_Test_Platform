from django.urls import path, include

urlpatterns = [
    path('users/', include('home.api.urls')),
    path('tests/', include('tests.api.urls'))
]