from rest_framework import serializers
from .models import Account, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


# ----------------- Register Serializer -----------------

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = Account.objects.create_user(
            email=email,
            password=password,
        )
        return user
    
# ----------------- LoginS erializer -----------------

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Both email and password are required")
        
        data['user'] = user
        return data
    


# ----------------- UserProfile Serializer -----------------

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name','bio', 'address', 'phone_number']

    
    
# ----------------- Account Serializer -----------------

class AccountSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'username',  'role', 'profile']

# ----------------- UserProfileUpdate Serializer -----------------

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'address', 'phone_number','first_name', 'last_name']


# ----------------- Change Password Serializer -----------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

# ----------------- Forget Password Serializer -----------------
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# ----------------- Reset Password Serializer -----------------
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True)  # token from email