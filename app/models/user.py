from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self,
            did,
            password,
            user_type,
            display_name,
            address,
            contact,
            email,
            birth=None):

        # Set FIELD
        if not did:
            raise ValueError('Users must have an ID')

        user = self.model(
            did = did,
            display_name = display_name,
            address = address,
            contact = contact,
            email = email,
            birth = birth,
            user_type = user_type,
        )

        # Set PASSWORD
        user.set_password(password)

        # Save USER
        user.save(using=self._db)
        return user

    def create_superuser(self, did, display_name, password):

        user = self.create_user(
            did = did,
            password = password,
            user_type = 5,
            display_name = display_name,
            address = "superuser",
            contact = "superuser",
            email = "superuser@example.com",
        )

        # Save USER
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    # Handler
    objects = UserManager()

    # PRIMARY
    did = models.CharField(
        max_length=128,
        unique=True,
        primary_key=True,
    )

    USERNAME_FIELD = 'did'

    # Customized
    # Required
    display_name = models.CharField(
        max_length=64,
    )
    address = models.CharField(
        max_length=128,
    )
    contact = models.CharField(
        max_length=32,
    )
    email = models.EmailField()
    user_type = models.SmallIntegerField()

    REQUIRED_FIELDS = [
        'display_name',
        'address',
        'contact',
        'email',
        'user_type',
    ]

    # Blankable
    birth = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # Django required
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
