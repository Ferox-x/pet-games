from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('games/', include('games.urls')),
    path('i18n', include('django.conf.urls.i18n')),
    path('support/', include('support.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('about.urls', namespace='about')),
    path('', include('core.urls', namespace='core')),
    path('__debug__/', include('debug_toolbar.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'
