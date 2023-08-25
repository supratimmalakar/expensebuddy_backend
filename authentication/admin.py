from django.contrib import admin
from .models import User, Buddyship, Buddy

class BuddyshipInline(admin.StackedInline):
    model = Buddyship
    fk_name = 'from_person'

class UserAdmin(admin.ModelAdmin):
    inlines = [BuddyshipInline]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Buddy)
# admin.site.register(Profile)
