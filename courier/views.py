from rest_framework import generics
from .serializers import RegisterSerializer,OrderSerializer,LoginSerializer,UserSerializer,ChangePasswordSerializer
from .models import User,Order
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
# import stripe
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from .renderers import UserRender
from rest_framework.permissions import IsAuthenticated



class RegisterView(generics.CreateAPIView):
    # renderer_classes=[UserRender] 
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            field = list(serializer.errors.keys())[0]
            # return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                    "success": False,
                    "errors": serializer.errors,
                    "field": field,
                    "message": "Invalid data! Please provide correct information."
                }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user_data = UserSerializer(user).data

        return Response({
            "success": True,
            "message": "User registered successfully.",
            "refresh_token": str(refresh),
            "access_token": str(access),
            "user_info": user_data
        }, status=status.HTTP_201_CREATED)



# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'admin'

# class IsDeliveryMan(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'delivery'

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get_permissions(self):
#         if self.action in ['assign_delivery', 'list_all']:
#             return [IsAdmin()]
#         elif self.action in ['update_status', 'my_deliveries']:
#             return [IsDeliveryMan()]
#         return [permissions.IsAuthenticated()]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         user = self.request.user
#         if user.role == 'admin':
#             return Order.objects.all()
#         elif user.role == 'delivery':
#             return Order.objects.filter(assigned_delivery_man=user)
#         return Order.objects.filter(user=user)

#     @action(detail=True, methods=['put'])
#     def assign_delivery(self, request, pk=None):
#         order = self.get_object()
#         delivery_id = request.data.get('delivery_man_id')
#         try:
#             delivery_man = User.objects.get(id=delivery_id, role='delivery')
#             order.assigned_delivery_man = delivery_man
#             order.status = 'assigned'
#             order.save()
#             return Response({"message": "Delivery man assigned."})
#         except:
#             return Response({"error": "Invalid delivery man ID."}, status=400)

#     @action(detail=True, methods=['put'])
#     def update_status(self, request, pk=None):
#         order = self.get_object()
#         if order.assigned_delivery_man != request.user:
#             return Response({"error": "Unauthorized."}, status=403)
#         status = request.data.get('status')
#         if status not in ['delivered', 'completed']:
#             return Response({"error": "Invalid status."}, status=400)
#         order.status = status
#         order.save()
#         return Response({"message": f"Status updated to {status}."})



# from decouple import config
# from rest_framework.views import APIView

# # stripe.api_key = settings.STRIPE_SECRET_KEY

# class StripePaymentView(APIView):
#     def post(self, request, format=None):
#         pass
        # try:
            # order_id = request.data.get('order_id')
            # order = Order.objects.get(id=order_id, user=request.user)

            # session = stripe.checkout.Session.create(
            #     payment_method_types=['card'],
            #     line_items=[{
            #         'price_data': {
            #             'currency': 'usd',
            #             'product_data': {'name': f'Order #{order.id}'},
            #             'unit_amount': int(order.delivery_fee * 100),
            #         },
            #         'quantity': 1,
            #     }],
            #     mode='payment',
            #     success_url='https://example.com/success',
            #     cancel_url='https://example.com/cancel',
            # )
            # return Response({'checkout_url': session.url})
        # except Exception as e:
        #     return Response({'error': str(e)}, status=400)
        
class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh_token':str(refresh),
                'access_token':str(refresh.access_token),
                'user_info': user_serializer.data
            },status=200)
        else:
            return Response({
                "wrong_submit":"invation Candential!",
                # 'errors':{'non_field_errors':['Email or password is not vali d']}
            },status=401)

class UserProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # শুধু লগইন করা user update করতে পারবে
        return self.request.user  

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": "Profile updated successfully ✅",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # শুধু লগইনকৃত ইউজার

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Password updated successfully ✅"},
            status=status.HTTP_200_OK
        )