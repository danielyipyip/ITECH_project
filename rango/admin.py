from django.contrib import admin
from rango.models import Category, Page, UserProfile, Comment

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class UserProfileAdmin(admin.ModelAdmin):
    profile_display = ('level',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Comment)