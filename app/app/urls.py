from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import (
    path,
    include
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('skills/', include('skill.urls')),

    # Spectacular URL's
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
