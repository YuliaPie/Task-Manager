from django.db import models


class BaseModelManager(models.Manager):
    def create_model_instance(self, name, **extra_fields):
        if not name:
            raise ValueError('The name field must be set')
        model_instance = self.model(name=name, **extra_fields)
        model_instance.save(using=self._db)
        return model_instance


class CustomStatusManager(BaseModelManager):
    def create_status(self, name, **extra_fields):
        return self.create_model_instance(name, **extra_fields)


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomStatusManager()

    def __str__(self):
        return self.name
