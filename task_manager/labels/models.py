from django.db import models
from django.db.models import Model


class CustomLabelManager(models.Manager):
    def create_label(self, name, **extra_fields):
        if not name:
            raise ValueError('The name field must be set')
        label = self.model(name=name, **extra_fields)
        label.save(using=self._db)
        return label


class Label(Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomLabelManager()

    def __str__(self):
        return self.name
