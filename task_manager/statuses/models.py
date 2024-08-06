from django.db import models
from django.db.models import Model


class CustomStatusManager(models.Manager):
    def create_status(self, name, **extra_fields):
        if not name:
            raise ValueError('The name field must be set')
        status = self.model(name=name, **extra_fields)
        status.save(using=self._db)
        return status


class Status(Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomStatusManager()

    def __str__(self):
        return self.name
