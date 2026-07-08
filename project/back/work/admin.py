from django.contrib import admin
from .models import Work, MainCategory, SubCategory, BrandClient, Project

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_category', 'is_vertical', 'order']

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sub_category', 'user', 'status', 'is_visible', 'created_at')
    list_filter = ('sub_category', 'status', 'is_visible')
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
