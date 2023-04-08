from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('team/', team, name='team'),
    path('signup1/', signup1, name='signup1'),
    path('signup2/', signup2, name='signup2'),
    path('signup3/<str:user_type>/', signup3, name='signup3'),
    path('login/', login_view, name='login'),
    path('dashboard/',dashboard,name='dashboard')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)