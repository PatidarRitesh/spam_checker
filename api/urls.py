# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from .views import UserRegistrationView

# # urlpatterns = [
# #     path('register/', UserRegistrationView.as_view(), name='register'),
# #     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# #     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# # ]
# from .views import CustomTokenObtainPairView

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),
#     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]


# # api/urls.py
# from django.urls import path
# from .views import register, UserRegistrationView, CustomTokenObtainPairView

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),
#     path('login/', CustomTokenObtainPairView.as_view(), name='login'),
# ]
# from django.urls import path
# from .views import register, UserRegistrationView, CustomTokenObtainPairView

# urlpatterns = [
#     path('register/', register, name='register'),  # POST request to register a new user
#     path('user-registration/', UserRegistrationView.as_view(), name='user-registration'),  # POST request using UserSerializer
#     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST request to get JWT tokens
# ]


from django.urls import path
from .views import register, UserRegistrationView, CustomTokenObtainPairView, ContactListCreateView, SpamReportListCreateView

urlpatterns = [
    path('register/', register, name='register'),  # POST request to register a new user
    path('user-registration/', UserRegistrationView.as_view(), name='user-registration'),  # POST request using UserSerializer
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST request to get JWT tokens
    
    # Contact-related URLs
    path('contacts/', ContactListCreateView.as_view(), name='contacts'),  # GET/POST request to manage contacts
    
    # Spam Report-related URLs
    path('spam-reports/', SpamReportListCreateView.as_view(), name='spam-reports'),  # GET/POST request to manage spam reports
]
