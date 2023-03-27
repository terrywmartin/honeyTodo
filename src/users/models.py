from django.db import models
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from household.models import HouseHold

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    #household_id = models.UUIDField(blank=False,null=False)
    household = models.ForeignKey(HouseHold,blank=False,null=True,on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.CharField(max_length=250,blank=True,null=True,default='')
    profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user-default.png')
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,primary_key=True,editable=False)
    household_admin = models.BooleanField(null=False,blank=False,default=False)


    def __str__(self):
        if self.nickname == '':
            return self.user.email
        else:
            return self.nickname

class UserSettings(models.Model):
    profile = models.OneToOneField(Profile,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.email
    
class PasswordToken(models.Model):
    token = models.UUIDField(null=False,blank=False)
    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    user_id = models.PositiveIntegerField(null=True)
    household_id = models.UUIDField(null=False,blank=False)
    is_staff = models.BooleanField(null=False, default=False)
    is_admin = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)
    token_life = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)