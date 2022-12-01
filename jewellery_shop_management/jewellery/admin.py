from django.contrib import admin
from . import models


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('unique_id','order', 'product', 'quantity', 'price', 'total', 'hand', 'finger', 'ring_size', 'measurement', 'display_metal_type', 'weight')
    ordering = ('order', 'unique_id')
    list_filter = ('order', 'product',)
    readonly_fields = ('unique_id',)
    list_editable = ('hand', 'finger', 'ring_size', 'measurement', 'weight')
    fieldsets = (
        ('General', {'fields': ('unique_id', 'order', 'product')}),
        ('Specifications', {'fields': (('hand', 'finger', 'ring_size', 'measurement', 'metal_type', 'weight'),)}),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_category', 'price')



class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'created_at')


admin.site.register(models.MetalType)
admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.ReviewProduct, ReviewProductAdmin)
