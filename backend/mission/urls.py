from django.urls import path
from .views import CustomLoginView
from knox.views import LoginView, LogoutView
from .views import CheckAuthView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('check_auth/', CheckAuthView.as_view(), name='check_auth'),
]