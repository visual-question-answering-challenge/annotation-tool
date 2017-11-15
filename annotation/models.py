from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    img_path = models.CharField(max_length=500)

    def __str__(self):
        return self.img_path


class PoolItem(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    is_done = models.BooleanField(False)


class Annotation(models.Model):
    pool_item = models.ForeignKey(PoolItem)
    question_text = models.CharField(max_length=600)
