from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Account, UserProfile
from .serializers import (
    RegisterSerializer,
    AccountSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer
)

# ----------------- Authentication -----------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: AccountSerializer},
        operation_id="register_user",
        tags=["Authentication"],
        operation_description="Register a new user and return JWT tokens"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token_data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response({
                "message": "Account created successfully!",
                "user": AccountSerializer(user).data,
                "token": token_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User password")
            }
        ),
        responses={200: AccountSerializer},
        operation_id="login_user",
        tags=["Authentication"],
        operation_description="Login user with email & password and return JWT tokens"
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            token_data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response({
                "message": "Login successful",
                "user": AccountSerializer(user).data,
                "token": token_data
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------- Profile -----------------
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: AccountSerializer},
        operation_id="get_user_profile",
        tags=["Profile"],
        operation_description="Retrieve a user's profile by ID"
    )
    def get(self, request, pk):
        try:
            user = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={200: UserProfileUpdateSerializer},
        operation_id="update_user_profile",
        tags=["Profile"],
        security=[{'Bearer': []}],
        operation_description="Update profile of logged-in user"
    )
    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "profile": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Password Management -----------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_id="change_password",
        tags=["Password"],
        operation_description="Change password for logged-in user"
    )
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


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer,
        responses={200: "Password reset email sent", 404: "User not found"},
        operation_id="forget_password",
        tags=["Password"],
        operation_description="Send password reset email with token link"
    )
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            token = get_random_string(50)
            user.profile.reset_password_token = token
            user.profile.save()

            reset_link = f"http://127.0.0.1:8000/swagger/?url=/api/v1/account/password/reset_api/&token={token}"
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={200: "Password reset successfully", 400: "Invalid token"},
        operation_id="reset_password",
        tags=["Password"],
        operation_description="Reset password using token from email link"
    )
    def post(self, request):
        data = request.data.copy()
        token = request.query_params.get('token')
        if token:
            data['token'] = token
        serializer = ResetPasswordSerializer(data=data)
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

            profile.reset_password_token = ''
            profile.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Account List -----------------
class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'username', 'role']
    ordering_fields = ['date_joined', 'email', 'username']
    ordering = ['-date_joined']

