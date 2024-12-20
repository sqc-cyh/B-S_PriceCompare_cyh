from django.urls import path
from . import users_views

urlpatterns = [
    path('create-user/', users_views.create_user, name = 'create-user'),
]