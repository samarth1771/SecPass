from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework_jwt.settings import api_settings
from django.db import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        # if username is None:
        #     raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    # def get_full_name(self):
    #     return self.username
    #
    # def get_short_name(self):
    #     return self.username

    def _generate_jwt_token(self):

        # dt = datetime.now() + timedelta(days=7)
        #
        # token = jwt.encode({
        #     'id': self.pk,
        #     'exp': int(dt.strftime('%d'))
        # }, settings.SECRET_KEY, algorithm='HS256')

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        # response = jwt_response_payload_handler(token, self)
        return token

        # return token.decode('utf-8')

