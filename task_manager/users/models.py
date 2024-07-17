from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, default='anonymous')
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.username
