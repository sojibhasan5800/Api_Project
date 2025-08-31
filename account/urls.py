from django.urls import path,include
from .views import RegisterView, UserProfileView,UserProfileUpdateView,LoginView,ChangePasswordView,ForgetPasswordView,ResetPasswordView,AccountListView

urlpatterns = [
   path('register_api/', RegisterView.as_view(), name='register'),
   path('login_api/', LoginView.as_view(), name='login'),
   path('profile_api/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
   path('profile/update_api/', UserProfileUpdateView.as_view(), name='user-profile-update'),
   path('password/change_api/', ChangePasswordView.as_view(), name='change-password'),
   path('password/forget_api/', ForgetPasswordView.as_view(), name='forget-password'),
   path('password/reset_api/', ResetPasswordView.as_view(), name='reset-password'),
   path('accounts_list_api/', AccountListView.as_view(), name='account-list'),
]
