from django.urls import path, include
from accounts.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePass, ResetPassEmail

urlpatterns = [
    path('register_user/', UserRegistrationView.as_view(), name='u_register'),
    path('login_user/', UserLoginView.as_view(), name='u_login'),
    path('data_user/', UserProfileView.as_view(), name='u_data'),
    path('change_password/', UserChangePass.as_view(), name='change_pass'),
    path('reset_password/', ResetPassEmail.as_view(), name='reset_pass'),
    path('reset_password/<uid>/<token>/', ResetPassEmail.as_view(), name='reset_pass'),

]
