from django.shortcuts import render
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer, UserDataSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import generate_access_token
import jwt, json
from rest_framework import status
from rest_framework import serializers
from .utils import get_user_obj
from .models import Buddy


# Create your views here.
class UserRegistrationAPIView(APIView):
	serializer_class = UserRegistrationSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		content = { 'message': 'Hello!' }
		return Response(content)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		try:
			if serializer.is_valid(raise_exception=True):
				new_user = serializer.save()
				if new_user:
					access_token = generate_access_token(new_user)
					data = { 'access_token': access_token }
					response = Response(data, status=status.HTTP_201_CREATED)
					return response
		except Exception as error:
			return Response(error.get_full_details(), status=status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def post(self, request):
		email = request.data.get('email', None)
		user_password = request.data.get('password', None)

		if not user_password:
			raise AuthenticationFailed('A user password is needed.')

		if not email:
			raise AuthenticationFailed('An user email is needed.')

		user_instance = authenticate(username=email, password=user_password)

		if not user_instance:
			return Response(data = {'message': 'Credentials not correct'}, status=status.HTTP_404_NOT_FOUND)

		if user_instance.is_active:
			user_access_token = generate_access_token(user_instance)
			user = get_user_obj(user_instance)
			data = { 'access_token': user_access_token, 'user' : user }
			response = Response(data, status=status.HTTP_202_ACCEPTED)
			response.set_cookie(key='access_token', value=user_access_token, httponly=True)
			return response


class SetContactAPI(APIView):
	def post(self, request):
		user_id = request.user_id
		user_model = get_user_model()
		user = user_model.objects.get(user_id=user_id)
		contacts = request.data['contacts']
		for contact in contacts:
			if user_model.objects.filter(phone_number = contact['phone_number']).exists():
				contact_user = user_model.objects.get(phone_number = contact['phone_number'])
				if user.buddies.filter(phone_number = contact['phone_number']).exists():
					existing_buddy = user.buddies.get(phone_number = contact['phone_number'])
					if existing_buddy.contact_name != contact['contact_name']:
						existing_buddy.contact_name =contact['contact_name']
						existing_buddy.save()
				else:
					buddy = Buddy(contact_name = contact['contact_name'], phone_number = contact['phone_number'], contact_user_id = contact_user.user_id , user = user)
					buddy.save()
		user_obj = get_user_obj(user)
		return Response(data = user_obj, status = status.HTTP_200_OK)


class UserViewAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		user_id = request.user_id
		user_model = get_user_model()
		user = user_model.objects.get(user_id=user_id)
		user_obj = get_user_obj(user)
		return Response(user_obj, status= status.HTTP_200_OK)
	
# check logic
# class UserProfileUpdateViewAPI(APIView):
# 	serializer_class = ProfileSerializer
# 	def post(self, request):
# 		serializer = self.serializer_class(data=request.data)
# 		if serializer.is_valid(raise_exception=True):
# 			updated_profile = serializer.save()
# 			return Response(data = updated_profile)
# 		else:
# 			return Response(data={"message": "Bad data"}, status = status.HTTP_400_BAD_REQUEST)
class UserDataUpdateViewAPI(APIView):
	# request should contain a list of fields that were updated called "request.data.updated_fields"
	def post(self, request):
		updated_fields = request.data["updated_fields"]
		user_id = request.user_id
		user_model = get_user_model()
		user = user_model.objects.get(user_id = user_id)
		for field in updated_fields:
			setattr(user, field, request.data[field])
		try:
			user.save()
			data = get_user_obj(user)
			return Response(data = data, status = status.HTTP_201_CREATED)
		except Exception as error:
			return Response(data = {"message": "Fields were not updated"}, status = status.HTTP_400_BAD_REQUEST)
		
				
class UserLogoutViewAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		user_token = request.COOKIES.get('access_token', None)
		if user_token:
			response = Response()
			response.delete_cookie('access_token')
			response.data = {
				'message': 'Logged out successfully.'
			}
			return response
		response = Response()
		response.data = {
			'message': 'User is already logged out.'
		}
		return response


