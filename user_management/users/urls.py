from django.urls import path
from .views import home, RegisterView, profile, user_table, block_user,unblock_user,delete_user

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'), 
    path('profile/', profile, name='users-profile'),
    path('user/', user_table, name='users-table'),
    path('block_user/', block_user, name='block_user'),
    path('unblock_user/', unblock_user, name='unblock_user'),
    path('delete_user/', delete_user, name='delete_user'),
]