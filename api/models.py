# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# # Custom user manager
# class UserManager(BaseUserManager):
#     def create_user(self, phone_number, name, password=None, email=None):
#         if not phone_number:
#             raise ValueError("Users must have a phone number")
#         if not name:
#             raise ValueError("Users must have a name")
        
#         user = self.model(phone_number=phone_number, name=name, email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, phone_number, name, password=None, email=None):
#         user = self.create_user(phone_number, name, password, email)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# # Custom User model
# class User(AbstractBaseUser):
#     phone_number = models.CharField(max_length=15, unique=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(null=True, blank=True, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.name

#     @property
#     def is_staff(self):
#         return self.is_admin


# # Contact model
# class Contact(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
#     phone_number = models.CharField(max_length=15)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.name} ({self.phone_number})"


# # Spam Report model
# class SpamReport(models.Model):
#     phone_number = models.CharField(max_length=15)
#     marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spam_reports')

#     def __str__(self):
#         return f"Spam: {self.phone_number} by {self.marked_by.name}"


# api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, email=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not name:
            raise ValueError("Users must have a name")
        
        user = self.model(phone_number=phone_number, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, email=None):
        user = self.create_user(phone_number, name, password, email)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin
