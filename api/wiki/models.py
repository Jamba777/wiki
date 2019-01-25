from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class PageModel(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField()


class VersionModel(models.Model):

    class Meta:
        ordering = ('-create_date', )

    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    current = models.BooleanField(default=True)
    page = models.ForeignKey('wiki.PageModel', related_name='page_versions', on_delete=models.CASCADE)
