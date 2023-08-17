from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("api/user" in request.get_full_path())
        if "api/user" in request.get_full_path():
            print("protected route")
            user_token = request.COOKIES.get('access_token')
            if not user_token:
                raise AuthenticationFailed('Unauthenticated user.')
            if user_token:
                try:
                    payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
                    request.user_id = payload['user_id']
                    return None
                except jwt.ExpiredSignatureError:
                    return Response(data = {"message": "Access Token has expired"}, status = status.HTTP_401_UNAUTHORIZED)
                except (jwt.DecodeError, jwt.InvalidTokenError):
                    return Response(data = {"message": "Authorization has failed"}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            print("unprotected route")
            return None
        
# user_token = request.COOKIES.get('access_token')

# 		if not user_token:
# 			raise AuthenticationFailed('Unauthenticated user.')

# 		payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])