from django.urls import path
from .views import index, team, signup1, signup2, signup3

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('team/', team, name='team'),
    path('signup1/', signup1, name='signup1'),
    path('signup2/', signup2, name='signup2'),
    path('signup3/<str:user_type>/', signup3, name='signup3'),
]