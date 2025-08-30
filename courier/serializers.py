from rest_framework import serializers
from .models import User,Order,UserProfile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_email(self, value):
        # Check for duplicate email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use. Please use a different email.")
        return value
    
    def validate_role(self, value):
        allowed_roles = ['user', 'admin', 'delivery']
        if value not in allowed_roles:
            raise serializers.ValidationError(f"Role must be one of {allowed_roles}.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'status', 'assigned_delivery_man', 'payment_completed']

 
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields=['id','email']





# Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        extra_kwargs = {
            'phone': {'required': False},
            'address': {'required': False},
            # 'dob': {'required': False},
        }

# User Serializer (Nested Profile)
# class UserList(serializers.ModelSerializer):
#     profile = UserProfileSerializer(read_only=True)  # Nested read

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'role', 'profile']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']
        read_only_fields = ['id', 'username', 'role']

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     user = User.objects.create(**validated_data)
    #     if profile_data:
    #         UserProfile.objects.create(user=user, **profile_data)
    #     return user

    def update(self, instance, validated_data):
        # profile data আলাদা করি
        profile_data = validated_data.pop('profile', None)

        # শুধু email আপডেট করার অনুমতি
        if 'email' in validated_data:
            instance.email = validated_data['email']
        instance.save()

        # Profile data update করি
        if profile_data:
            UserProfile.objects.update_or_create(
                user=instance,
                defaults=profile_data
            )

        return instance




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Password validation check
        password_validation.validate_password(value)
        return value