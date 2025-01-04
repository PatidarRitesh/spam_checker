# from rest_framework import serializers
# from .models import User, Contact, SpamReport
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'phone_number', 'email', 'name', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             phone_number=validated_data['phone_number'],
#             name=validated_data['name'],
#             email=validated_data.get('email', ''),
#             password=validated_data['password']
#         )
#         return user

# from rest_framework import serializers
# from .models import Contact

# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ['id', 'name', 'phone_number', 'email', 'user']  # Assuming 'user' should be part of the serializer
#         extra_kwargs = {'user': {'read_only': True}}

#     def create(self, validated_data):
#         # Extract the user from the context and ensure it's not in validated_data
#         user = self.context['request'].user
#         # Remove 'user' from validated_data if it accidentally got included
#         validated_data.pop('user', None)  # Safely remove 'user' key if exists
        
#         return Contact.objects.create(user=user, **validated_data)

# from rest_framework import serializers
# from .models import SpamReport

# class SpamReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SpamReport
#         fields = ['phone_number', 'is_spam', 'user']
#         extra_kwargs = {'user': {'read_only': True}}

#     def create(self, validated_data):
#         print("Available context keys:", self.context.keys())  # Should list 'request' among other keys

#         user = self.context['request'].user
#         return SpamReport.objects.create(user=user, **validated_data)

# class UserSerializer(serializers.ModelSerializer):
#     spam_likelihood = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['id', 'phone_number', 'email', 'name', 'spam_likelihood']

#     def get_spam_likelihood(self, obj):
#         return SpamReport.spam_likelihood(obj.phone_number)


# from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import User
# from django.contrib.auth import authenticate

# class CustomTokenObtainPairSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         phone_number = attrs.get('phone_number')
#         password = attrs.get('password')

#         # Authenticate the user based on phone_number
#         user = authenticate(username=phone_number, password=password)
#         if user is None:
#             raise serializers.ValidationError("Invalid phone number or password.")

#         # Generate refresh and access tokens for the user
#         refresh = RefreshToken.for_user(user)
#         return {
#             'access': str(refresh.access_token),
#             'refresh': str(refresh)
#         }


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Contact, SpamReport


# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'name', 'password', 'spam_likelihood']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

    def get_spam_likelihood(self, obj):
        # Fetch spam likelihood based on phone number
        return SpamReport.spam_likelihood(obj.phone_number)


# ContactSerializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email', 'user']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # Remove 'user' if present in data
        return Contact.objects.create(user=user, **validated_data)


# SpamReportSerializer
class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['phone_number', 'is_spam', 'user']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        return SpamReport.objects.create(user=user, **validated_data)


# CustomTokenObtainPairSerializer
class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid phone number or password.")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
