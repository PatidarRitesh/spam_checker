
# api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Count

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


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.phone_number})'


# class SpamReport(models.Model):
#     user = models.ForeignKey(User, related_name='spam_reports', on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15)
#     is_spam = models.BooleanField(default=False)
#     reported_on = models.DateTimeField(auto_now_add=True)

#     @classmethod
#     def spam_likelihood(cls, phone_number):
#         reports = cls.objects.filter(phone_number=phone_number)
#         total_reports = reports.count()
#         spam_reports = reports.filter(is_spam=True).count()

#         if total_reports == 0:
#             return 0.0  # No reports, no likelihood
#         return round((spam_reports / total_reports) * 100, 2)  # Return percentage rounded to 2 decimals


class SpamReport(models.Model):
    user = models.ForeignKey(User, related_name='spam_reports', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_spam = models.BooleanField(default=False)
    reported_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def spam_likelihood(cls, phone_number):
        reports = cls.objects.filter(phone_number=phone_number)
        total_reports = reports.count()
        spam_reports = reports.filter(is_spam=True).count()

        if total_reports == 0:
            return 0.0  # No reports, no likelihood
        return round((spam_reports / total_reports) * 100, 2)  # Percentage rounded to 2 decimals
