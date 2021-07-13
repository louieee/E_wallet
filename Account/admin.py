from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Source)
admin.site.register(Cache)