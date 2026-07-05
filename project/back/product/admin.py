from django.contrib import admin
from .models import Plan, Recommend, Operation, Production, Item

admin.site.register(Recommend)
admin.site.register(Operation)
admin.site.register(Production)
admin.site.register(Item)

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'name', 'price', 'created_at')
    filter_horizontal = ('recommends', 'operations', 'productions', 'items')
