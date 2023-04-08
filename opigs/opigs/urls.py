from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', logout_view, name='admin_logout'),
    path('', include('core.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
