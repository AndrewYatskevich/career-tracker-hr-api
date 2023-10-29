from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import CustomUser

admin.site.register(CustomUser)
admin.site.unregister(Group)
