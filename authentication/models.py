from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver 
from django.db.models.signals import post_save #add this


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('A user email is needed.')

        if not password:
            raise ValueError('A user password is needed.')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('A user email is needed.')

        if not password:
            raise ValueError('A user password is needed.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_onboarded = models.BooleanField(default=False)
    buddyships = models.ManyToManyField('self', through='Buddyship',
                                           symmetrical=False,
                                           related_name='related_to+')
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def add_buddyship(self, user, symm=True):
        buddyship, create = Buddyship.objects.get_or_create(
            from_person = self,
            to_person = user
        )
        if symm:
            user.add_buddyship(self, False)
    
    def get_buddyships(self):
        return self.buddyships.filter(
            to_people__from_person=self)

class Buddyship(models.Model):
    from_person = models.ForeignKey(User, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(User, related_name='to_people', on_delete=models.CASCADE)

