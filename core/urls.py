from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from rest_framework.routers import DefaultRouter

# fcm push notifications urls
router = DefaultRouter()

swagger_urlpatterns = [

    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentications.urls")),
    # app urls
    path("api/notices/", include("notice.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("tour/", include("tour_planner.urls")),
]
# serving media and static files
media_url = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

fcm_urls = [
    # path('api/devices/', FCMDeviceAuthorizedViewSet.as_view(), name='create_fcm_device'),
]
# serving media and static files and swagger
urlpatterns += media_url
# urlpatterns += fcm_urls
urlpatterns += router.urls
if settings.DEBUG and not settings.APP_ON_PRODUCTION:
    urlpatterns += swagger_urlpatterns
    # if app is in debug mode enable django toolbar

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
