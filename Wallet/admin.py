from django.contrib import admin
from.models import *
# Register your models here.



# this allows all the models in the wallet section to be accessible in the admin page
admin.site.register(Wallet)
admin.site.register(Transaction)