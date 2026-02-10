from django.contrib import admin
from restaurant_app.models import Category, ContactMessage, Order, OrderItem, Product, Profile, Reservation


# Register your models here.
admin.site.register(Category)
admin.site.register(ContactMessage)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Reservation)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'full_name', 'email', 'phone']
    inlines = [OrderItemInline]
