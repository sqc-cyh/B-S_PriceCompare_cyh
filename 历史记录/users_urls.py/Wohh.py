from django.urls import path
from . import users_views

urlpatterns = [
    path('all-cashier/', users_views.all_cashiers, name = 'all-cashiers'),
    # path('add/', users_views.add_cashier, name = 'add_cashier'),
    # path('delete/', users_views.delete_cashier, name = 'delete_cashier'),
    # path('modify-base/', users_views.modify_cashier, name = 'modify_cashier'),
    # path('modify-authority/', users_views.modify_authority, name = 'modify_authority')
]