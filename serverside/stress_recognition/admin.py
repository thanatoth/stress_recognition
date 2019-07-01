from django.contrib import admin

# Register your models here.

from .models import User, UserCondition, Photo

admin.site.register(User)
admin.site.register(UserCondition)
admin.site.register(Photo)
