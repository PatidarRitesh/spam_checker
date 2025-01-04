

# from django.urls import path
# from .views import register, UserRegistrationView, CustomTokenObtainPairView, ContactListCreateView, SpamReportListCreateView,SpamReportView
# from .views import SearchByNameView, SearchByPhoneNumberView   ,   SearchByNameView,SearchByPhoneNumberView
# urlpatterns = [
#     path('register/', register, name='register'),  # POST request to register a new user
#     path('user-registration/', UserRegistrationView.as_view(), name='user-registration'),  # POST request using UserSerializer
#     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST request to get JWT tokens
    
#     # Contact-related URLs
#     path('contacts/', ContactListCreateView.as_view(), name='contacts'),  # GET/POST request to manage contacts
    
#     # Spam Report-related URLs
#     # path('spam-reports/', SpamReportListCreateView.as_view(), name='spam-reports'),  # GET/POST request to manage spam reports
#     path('spam-reports/', SpamReportView.as_view(), name='spam-reports'),

#     path('search/name/', SearchByNameView.as_view(), name='search-by-name'),
#    path('search/phone-number/', SearchByPhoneNumberView.as_view(), name='search-by-phone-number'),

# ]


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
