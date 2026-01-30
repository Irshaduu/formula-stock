from django.contrib import admin
from .models import Category, SubCategory, Item, ConsumptionRecord

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'current_stock', 'average_stock', 'score')
    list_filter = ('category', 'subcategory')
    search_fields = ('name',)

@admin.register(ConsumptionRecord)
class ConsumptionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'date', 'timestamp')
    list_filter = ('user', 'date', 'item__category')
    date_hierarchy = 'date'
