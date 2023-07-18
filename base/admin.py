from django.contrib import admin
from .models import User, Indecision, Field, Status

# Register your models here.
admin.site.register(Indecision)
admin.site.register(Field)
admin.site.register(Status)
