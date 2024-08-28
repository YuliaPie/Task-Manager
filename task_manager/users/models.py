from django.db import models
from django.contrib.auth.models import (AbstractUser,
                                        PermissionsMixin)


class CustomUser(AbstractUser, PermissionsMixin):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    def __str__(self):
        return self.get_full_name()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = False
