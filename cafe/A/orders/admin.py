from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tables', 'number', 'status', 'timestamp', 'users', 'receipts', 'menu_items')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('total_price', 'final_price', 'timestamp', 'users')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'discount', 'serving_time_period', 'estimated_time')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'cafe_space_position', 'use')
