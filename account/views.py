from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AccountSerializer
from .models import Account
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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