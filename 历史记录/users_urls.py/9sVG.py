from django.urls import path
from . import users_views

urlpatterns = [
    path('create-user/', users_views.create_user, name = 'create-user'),
    # path('add/', users_views.add_cashier, name = 'add_cashier'),
    # path('delete/', users_views.delete_cashier, name = 'delete_cashier'),
    # path('modify-base/', users_views.modify_cashier, name = 'modify_cashier'),
    # path('modify-authority/', users_views.modify_authority, name = 'modify_authority')
]