from django.urls import path
from .views import index, team, register

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('team/', team, name='team'),
    path('register/', register, name='register')
]