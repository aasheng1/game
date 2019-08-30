from django.contrib import admin

# Register your models here.
from .models import GameDetails,GameClass,Publishers

admin.site.register(GameDetails)
admin.site.register(GameClass)
admin.site.register(Publishers)