from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.User)
admin.site.register(models.Recipemail)
admin.site.register(models.adressbook)
admin.site.register(models.Sendemail)