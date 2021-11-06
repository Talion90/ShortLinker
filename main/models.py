from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    long_link = models.URLField(unique=True)
    short_link = models.URLField(unique=True)
    token = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.long_link
