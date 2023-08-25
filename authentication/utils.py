from django.conf import settings
from datetime import datetime, timedelta
import jwt


def generate_access_token(user):
	payload = {
		'user_id': user.user_id,
		'exp': datetime.utcnow() + timedelta(days=1, minutes=0),
		'iat': datetime.utcnow(),
	}

	access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
	return access_token

def get_user_obj(user_instance):
	buddies = []
	for buddy in user_instance.buddies.all():
		buddies.append({'contact_name' : buddy.contact_name, 'phone_number' : buddy.phone_number })
	data = {
				'email' : user_instance.email,
				'first_name': user_instance.first_name,
				'last_name': user_instance.last_name,
				'is_onboarded': user_instance.is_onboarded,
				'contact_count': user_instance.contact_count,
				'phone_number': user_instance.phone_number,
				'buddies': buddies,
			}
	return data