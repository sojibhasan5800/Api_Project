from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AccountSerializer,ChangePasswordSerializer,ForgetPasswordSerializer,ResetPasswordSerializer
from .models import Account,UserProfile
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# ----------------- Register View -----------------
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
             # JWT Token generate
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

            return Response({
                "message": "Account created successfully!",
                "user": AccountSerializer(user).data,
                "token": token_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# ----------------- Login View -----------------
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response({
                "message": "Login successful",
                "user": AccountSerializer(user).data,
                "token": token_data
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------- Profile View -----------------

class UserProfileView(APIView):
    def get(self, request, pk):
        try:
            user = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------- Profile Update -----------------

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # only logged-in users can access

    def put(self, request):
        profile = request.user.profile  # get the profile of the logged-in user
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ----------------- Change Password -----------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Forget Password -----------------
class ForgetPasswordView(APIView):
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Generate a temporary token 
            token = get_random_string(50)
            user.profile.reset_password_token = token
            user.profile.save()

            reset_link = f"http://your-frontend-domain/reset-password/?token={token}"
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                'your_gmail@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Reset Password -----------------
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                profile = UserProfile.objects.get(reset_password_token=token)
            except UserProfile.DoesNotExist:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            user = profile.user
            user.set_password(new_password)
            user.save()

            # Clear token
            profile.reset_password_token = ''
            profile.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)