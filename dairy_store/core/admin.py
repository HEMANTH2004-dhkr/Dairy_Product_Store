from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, UserProfile
# ⛔ Don't re-import CartItem here

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'preview_image']
    search_fields = ['name']
    list_filter = ['category']

    def preview_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover;" />')
        return "No Image"
    preview_image.short_description = 'Image'

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(UserProfile)
# ✅ Don't register CartItem again here