from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('accounts/', include('allauth.urls')),
]
handler404 = 'product.views.custom_page_not_found_view'
# handler500 = 'my_app_name.views.custom_error_view'
# handler403 = 'my_app_name.views.custom_permission_denied_view'
# handler400 = 'my_app_name.views.custom_bad_request_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)