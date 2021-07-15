from django.contrib import admin
from .models import *
# Register your models here.

# this allows the models in the account section to be accessible in the admin's page

admin.site.register(User)
admin.site.register(Card)
admin.site.register(Source)
admin.site.register(Cache)