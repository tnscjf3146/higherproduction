from django.contrib import admin
from .models import Work, Category, BrandClient, Project

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'is_vertical')
    list_editable = ('order', 'is_vertical')

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'user', 'status', 'is_visible', 'created_at')
    list_filter = ('category', 'status', 'is_visible')
    search_fields = ('title', 'user__username', 'user__email')

@admin.register(BrandClient)
class BrandClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'client', 'created_at')
    list_filter = ('client',)
    search_fields = ('title', 'client__name')
