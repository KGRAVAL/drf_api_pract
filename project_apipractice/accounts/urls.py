from django.urls import path, include
from accounts.views import UserRegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    path('register_user/', UserRegistrationView.as_view(), name='u_register'),
    path('login_user/', UserLoginView.as_view(), name='u_login'),
    path('data_user/', UserProfileView.as_view(), name='u_data'),


]
