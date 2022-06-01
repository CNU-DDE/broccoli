from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import json
import hashlib

DEFAULT_USER_TYPE=3

class UserManager(BaseUserManager):
    def create_user(self,
            identifier,
            display_name,
            password,
            keystore,
            email,
            user_type=DEFAULT_USER_TYPE):

        # Set FIELD
        if not identifier:
            raise ValueError('Users must have an ID')

        user = self.model(
            identifier = identifier,
            user_type = user_type,
            display_name = display_name,
            email = email,
        )

        # Set PASSWORD
        user.set_password(self.create_digest(password, keystore))

        # Save USER
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, display_name, password):

        user = self.create_user(identifier, display_name, password, None, "no-email@example.com", 5)

        # Save USER
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_digest(self, password, keystore=None):

        # Keystore not provided
        if not keystore:
            return hashlib.sha256(password).hexdigest()

        # Keystore provided
        JSON = json.dumps({
            "password": password,
            "keystore": keystore,
        }, sort_keys=True).encode('utf8')

        return hashlib.sha256(JSON).hexdigest()

class User(AbstractBaseUser):

    # PRIMARY
    identifier = models.CharField(
        verbose_name='id',
        max_length=72,
        unique=True,
        primary_key=True,
    )

    # Customized
    user_type = models.SmallIntegerField(default=3)
    display_name = models.CharField(max_length=255)
    email = models.EmailField(default=None)

    # Django required
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Configurations
    objects = UserManager()

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
