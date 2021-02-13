from django.contrib import admin
from .models import Category, Photo


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'place_name')
    list_display_links = ('id', 'place_name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)
