from django.contrib import admin
from .models import Image, Annotation, PoolItem

admin.site.register(Image)
admin.site.register(Annotation)
admin.site.register(PoolItem)