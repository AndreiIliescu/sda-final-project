from django.contrib import admin
from restaurant_app.models import Category, ContactMessage, Product, Profile, Reservation


# Register your models here.
admin.site.register(Category)
admin.site.register(ContactMessage)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Reservation)
