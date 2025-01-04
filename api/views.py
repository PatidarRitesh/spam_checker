# # api/views.py
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.conf import settings
# # api/views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializers import UserSerializer

# User = settings.AUTH_USER_MODEL
# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         # Get data from request
#         name = request.data.get('name')
#         phone_number = request.data.get('phone_number')
#         email = request.data.get('email', None)
#         password = request.data.get('password')

#         # Check if all required fields are provided
#         if not name or not phone_number or not password:
#             return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the phone number is already in use
#         if User.objects.filter(username=phone_number).exists():
#             return Response({"detail": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create a new user
#         user = User.objects.create_user(username=phone_number, password=password, email=email, first_name=name)

#         # Generate tokens (if needed)
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh)
#         }, status=status.HTTP_201_CREATED)



# class UserRegistrationView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class CustomTokenObtainPairSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         phone_number = attrs.get('phone_number')
#         password = attrs.get('password')

#         try:
#             user = User.objects.get(phone_number=phone_number)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Invalid phone number or password")

#         if not user.check_password(password):
#             raise serializers.ValidationError("Invalid phone number or password")

#         refresh = RefreshToken.for_user(user)
#         return {
#             'access': str(refresh.access_token),
#             'refresh': str(refresh)
#         }

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


# api/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.contrib.auth import authenticate
# from django.conf import settings
from .serializers import UserSerializer

from .models import User


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        # Get data from request
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email', None)
        password = request.data.get('password')

        # Check if all required fields are provided
        if not name or not phone_number or not password:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the phone number is already in use
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create_user(phone_number=phone_number, password=password, email=email, name=name)

        # Generate tokens (if needed)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        try:
            # Try to fetch the user by phone_number, assuming phone_number is the unique identifier
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number or password")

        # Check if the provided password is correct
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid phone number or password")

        # Generate refresh and access tokens for the user
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
