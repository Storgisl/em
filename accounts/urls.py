from django.urls import path
from .views import register_view, login_view, account_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
        path('logout/', logout_view, name='logout'),
    path('', account_view, name='account'),
]
