# # api/serializers.py
# from rest_framework import serializers
# from django.conf import settings

# User = settings.AUTH_USER_MODEL

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email', ''),
#             first_name=validated_data.get('first_name', ''),
#             password=validated_data['password']
#         )
#         return user
# api/serializers.py
# from rest_framework import serializers
# from .models import User

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




from rest_framework import serializers
from .models import User, Contact, SpamReport

# UserSerializer (already present)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'name', 'password']
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


# New ContactSerializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_number', 'name', 'email']

    def create(self, validated_data):
        contact = Contact.objects.create(
            user=validated_data['user'],
            phone_number=validated_data['phone_number'],
            name=validated_data.get('name', ''),
            email=validated_data.get('email', '')
        )
        return contact


# New SpamReportSerializer
class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['id', 'phone_number', 'is_spam', 'reported_on']

    def create(self, validated_data):
        spam_report = SpamReport.objects.create(
            user=validated_data['user'],
            phone_number=validated_data['phone_number'],
            is_spam=validated_data['is_spam']
        )
        return spam_report
