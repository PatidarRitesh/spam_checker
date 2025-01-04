
from django.urls import path
from .views import (
    register,
    UserRegistrationView,
    CustomTokenObtainPairView,
    ContactListCreateView,
    SpamReportView,
    SearchByNameView,
    SearchByPhoneNumberView
)

urlpatterns = [
    path('register/', register, name='register'),
    path('user-registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Contact-related URLs
    path('contacts/', ContactListCreateView.as_view(), name='contacts'),

    # Spam Report-related URLs
    path('spam-reports/', SpamReportView.as_view(), name='spam-reports'),

    # Search URLs
    path('search/name/', SearchByNameView.as_view(), name='search-by-name'),
    path('search/phone-number/', SearchByPhoneNumberView.as_view(), name='search-by-phone-number'),
]
