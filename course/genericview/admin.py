from django.contrib import admin

from .models import Cat, Horse, Dog

# Register your models here.

admin.site.register(Cat)
admin.site.register(Horse)
admin.site.register(Dog)