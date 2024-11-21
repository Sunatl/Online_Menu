from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  
    search_fields = ('name',) 
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')  
    search_fields = ('name',)  


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'create_at')
    list_filter = ('category', 'is_active')  
    search_fields = ('name',)  


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'status')  
    list_filter = ('status',)
    search_fields = ('table_name',) 


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('customer', 'table', 'total_sum', 'create_at', 'is_paid')  
    search_fields = ('customer__name', 'table__table_name')  
    list_filter = ('create_at', 'is_paid')  


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bill', 'menu_item', 'quantity')  
    search_fields = ('bill__customer__name', 'menu_item__name')  


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'bill', 'amount', 'method', 'date')  
    search_fields = ('customer__name', 'bill__id')  
    list_filter = ('method', 'date')  
