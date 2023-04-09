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
    path('success/', success, name='success'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard_S/', dashboard_S, name='dashboard_S'),
    path('dashboard_A/', dashboard_A, name='dashboard_A'),
    path('dashboard_C', dashboard_C, name='dashboard_C'),
    path('chat/<str:username>/', chat_view, name='chat'),
    path('send_chat/<str:username>', send_chat, name='send_chat'),
    path('search_results/', search_results, name='search_results'),
    path('create_application/<str:username>', create_application, name='create_application'),
    path('remove_application/<str:username>', remove_application, name='remove_application'),
    path('shortlist_application/<str:username>', shortlist_application, name='shortlist_application'),
    path('edit/', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)