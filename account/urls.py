from django.urls import path,include
from .views import RegisterView, UserProfileView,UserProfileUpdateView,LoginView

urlpatterns = [
   path('register_api/', RegisterView.as_view(), name='register'),
   path('login_api/', LoginView.as_view(), name='login'),
   path('profile_api/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
   path('profile/update_api/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]
