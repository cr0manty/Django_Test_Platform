from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('tests/', include('tests.urls')),
    path('api/', include('api.urls')),
    path('/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += [
        path('media/<path>', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
