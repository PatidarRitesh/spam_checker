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
