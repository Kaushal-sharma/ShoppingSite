from django.contrib import admin
from site_app.models import Product, Cart, Customer, OrderPlaced
# import by programmer
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discount_price', 'description', 'brand', 'category', 'product_image']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'address', 'zipcode', 'city', 'state']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'order_date', 'delivery_date', 'quantity', 'price', 'status']
