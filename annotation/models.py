from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    img_path = models.CharField(max_length=500)
    visual_genome_url = models.URLField()

    def __str__(self):
        return self.img_path


class Annotation(models.Model):
    fk_user = models.ForeignKey(User)
    fk_image = models.ForeignKey(Image)
    question_text = models.CharField(max_length=600)
