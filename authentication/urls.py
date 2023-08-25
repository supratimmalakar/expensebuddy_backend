from django.urls import path
from authentication.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	UserLogoutViewAPI,
    UserDataUpdateViewAPI,
    SetContactAPI
)

urlpatterns = [
	path('register/', UserRegistrationAPIView.as_view()),
	path('login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	path('user/logout/', UserLogoutViewAPI.as_view()),
    path('user/update_profile/', UserDataUpdateViewAPI.as_view()),
    path('user/set_contacts/', SetContactAPI.as_view())
]
