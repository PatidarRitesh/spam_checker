from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .serializers import UserSerializer
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.permissions import IsAuthenticated
from .serializers import ContactSerializer
from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response

  

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        # Extract data from request
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email', None)
        password = request.data.get('password')

        # Validate required fields
        if not name or not phone_number or not password:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure phone number and email uniqueness
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "Phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if email and User.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new user
            user = User.objects.create_user(phone_number=phone_number, password=password, email=email, name=name)
            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle other unforeseen integrity issues
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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




class ContactListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)  # Manually set the user from request.user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Spam Report API Views
class SpamReportListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the logged-in user's spam reports
        spam_reports = SpamReport.objects.filter(user=request.user)
        serializer = SpamReportSerializer(spam_reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new spam report for the logged-in user
        request.data['user'] = request.user.id  # Automatically associate the user with the spam report
        serializer = SpamReportSerializer(data=request.data)
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


class SpamReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("Passing request in context:", 'request' in {'request': request})  # Should print True
        serializer = SpamReportSerializer(data=request.data, context={'request': request})
        print("Serializer context keys after instantiation:", serializer.context.keys())  # Should include 'request'
    # Proceed with validation and saving...

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

from django.db.models import Q
from django.db.models import Case, When, Value, FloatField
from django.db.models.functions import Lower
from django.db.models import F


from django.db.models import Count, Case, When


from django.db import models
# class SearchByNameView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         query = request.query_params.get('name')
#         if not query:
#             return Response({"error": "A search query is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Normalize query
#         query = query.strip()

#         # Search registered users
#         users = User.objects.filter(name__icontains=query).annotate(
#             spam_likelihood=Count(
#                 'spam_reports',
#                 filter=models.Q(spam_reports__is_spam=True)
#             ) * 100 / Count('spam_reports', distinct=True)
#         ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

#         # Search contacts of the logged-in user
#         contacts = Contact.objects.filter(user=request.user, name__icontains=query).annotate(
#             spam_likelihood=Count(
#                 'user__spam_reports',
#                 filter=models.Q(user__spam_reports__is_spam=True)
#             ) * 100 / Count('user__spam_reports', distinct=True)
#         ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

#         # Combine and sort results: prioritize names starting with the query, then others
#         combined_results = list(users) + list(contacts)
#         combined_results.sort(key=lambda x: (not x['name'].lower().startswith(query.lower()), x['name'].lower()))

#         return Response(combined_results, status=status.HTTP_200_OK)
from django.db.models import F, Case, When, Value, FloatField
from django.db.models.functions import Coalesce

class SearchByNameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('name')
        if not query:
            return Response({"error": "A search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Search registered users
        users = User.objects.filter(name__icontains=query).annotate(
            spam_likelihood=Coalesce(
                Count('spam_reports', filter=Q(spam_reports__is_spam=True)) * 100.0 / Count('spam_reports'),
                0.0,
                output_field=FloatField()
            )
        ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

        # Search contacts of the logged-in user
        contacts = Contact.objects.filter(user=request.user, name__icontains=query).annotate(
            spam_likelihood=Coalesce(
                Count('user__spam_reports', filter=Q(user__spam_reports__is_spam=True)) * 100.0 / Count('user__spam_reports'),
                0.0,
                output_field=FloatField()
            )
        ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

        # Combine and sort results
        combined_results = list(users) + list(contacts)
        combined_results.sort(key=lambda x: (not x['name'].lower().startswith(query.lower()), x['name'].lower()))

        return Response(combined_results, status=status.HTTP_200_OK)





def normalize_phone_number(phone_number):
    """
    Normalize phone number by ensuring a consistent format.
    Strips spaces and ensures '+' prefix.
    """
    phone_number = phone_number.strip()
    if not phone_number.startswith('+'):
        phone_number = f"+{phone_number}"
    return phone_number


# class SearchByPhoneNumberView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         phone_number = request.query_params.get('phone_number')
#         if not phone_number:
#             return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Normalize phone number
#         phone_number = normalize_phone_number(phone_number)
#         print(f"Normalized phone number for search: {phone_number}")

#         # Search for registered users
#         registered_users = User.objects.filter(phone_number=phone_number).annotate(
#             spam_likelihood=Count(
#                 'spam_reports',
#                 filter=models.Q(spam_reports__is_spam=True)
#             ) * 100 / Count('spam_reports', distinct=True)
#         ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

#         # Search contacts for the logged-in user
#         contacts = Contact.objects.filter(user=request.user, phone_number=phone_number).annotate(
#             spam_likelihood=Count(
#                 'user__spam_reports',
#                 filter=models.Q(user__spam_reports__is_spam=True)
#             ) * 100 / Count('user__spam_reports', distinct=True)
#         ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

#         # Combine results if both exist
#         combined_results = list(registered_users) + list(contacts)

#         if combined_results:
#             return Response(combined_results, status=status.HTTP_200_OK)

#         return Response({"error": "Phone number not found."}, status=status.HTTP_404_NOT_FOUND)


class SearchByPhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone_number = request.query_params.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = normalize_phone_number(phone_number)

        # Search for registered users
        registered_users = User.objects.filter(phone_number=phone_number).annotate(
            spam_likelihood=Coalesce(
                Count('spam_reports', filter=Q(spam_reports__is_spam=True)) * 100.0 / Count('spam_reports'),
                0.0,
                output_field=FloatField()
            )
        ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

        # Search contacts for the logged-in user
        contacts = Contact.objects.filter(user=request.user, phone_number=phone_number).annotate(
            spam_likelihood=Coalesce(
                Count('user__spam_reports', filter=Q(user__spam_reports__is_spam=True)) * 100.0 / Count('user__spam_reports'),
                0.0,
                output_field=FloatField()
            )
        ).values('id', 'name', 'phone_number', 'email', 'spam_likelihood')

        # Combine results
        combined_results = list(registered_users) + list(contacts)

        if combined_results:
            return Response(combined_results, status=status.HTTP_200_OK)
        # Return NO contact found in database and status code 200
        return Response({"Phone number not found in Database"}, status=status.HTTP_200_OK)
        
