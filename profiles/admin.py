from django.contrib import admin
from .models import UserProfile


# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


admin.site.register(UserProfile)
