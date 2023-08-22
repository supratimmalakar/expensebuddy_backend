from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	class Meta:
		model = get_user_model()
		fields = ['email', 'password', 'first_name', 'last_name', 'is_onboarded']

	def create(self, validated_data):
		user_password = validated_data.get('password', None)
		db_instance = self.Meta.model(email=validated_data.get('email'))
		db_instance.set_password(user_password)
		db_instance.first_name = validated_data.get('first_name', None)
		db_instance.last_name = validated_data.get('last_name', None)
		db_instance.save()
		return db_instance
	
	def update(self, instance, validated_data):
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.is_onboarded = validated_data.get('is_onboarded', instance.is_onboarded)
		instance.email = validated_data.get('email', instance.email)
		instance.save()
		return instance

	


class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=100)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	token = serializers.CharField(max_length=255, read_only=True)

class UserDataSerializer(serializers.Serializer):
	class Meta:
		model = get_user_model()
		fields = "__all__"

	# def create(self, validated_data):
	# 	return self.Meta.model.objects.create(**validated_data)
	
	# # def create(self, validated_data):
    # #     return model.objects.create(**validated_data)

	# def update(self, instance, validated_data):
	# 	instance.first_name = validated_data.get('first_name', instance.first_name)
	# 	instance.last_name = validated_data.get('last_name', instance.last_name)
	# 	instance.is_onboarded = validated_data.get('is_onboarded', instance.is_onboarded)
	# 	instance.email = validated_data.get('email', instance.email)
	# 	instance.save()
	# 	return instance
	
# class ProfileSerializer(serializers.Serializer):
# 	class Meta:
# 		model = Profile
# 		fields = ["first_name", "last_name", "is_onboarded"]