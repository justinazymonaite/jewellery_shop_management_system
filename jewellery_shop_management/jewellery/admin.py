from django.contrib import admin
from . import models


class OrderLineInline(admin.StackedInline):
    model = models.OrderLine
    extra = 0
    readonly_fields = ('unique_id', )
    can_delete = False


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('unique_id','order', 'product', 'quantity','hand', 'finger', 'ring_size', 'display_metal_type', 'weight')
    ordering = ('order', 'unique_id')
    list_filter = ('order', 'product',)
    readonly_fields = ('unique_id',)
    list_editable = ('hand', 'finger', 'ring_size', 'weight')
    fieldsets = (
        ('General', {'fields': ('unique_id', 'order', 'product', 'quantity')}),
        ('Specifications', {'fields': ('hand', 'finger', 'ring_size', 'measurement', 'metal_type', 'pearl', 'weight', 'photo', 'specification', 'engraving', 'engraving_file')}),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    readonly_fields = ('is_overdue', 'date', 'is_overdue' )
    inlines = (OrderLineInline, )
    list_editable = ('status', 'due_date')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'jewellery_type', 'display_category', 'price')


class PearlAdmin(admin.ModelAdmin):
    list_display = ('parcel', 'shape', 'color', 'size', 'type_name',)
    list_filter = ('shape', 'color')


class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'created_at')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


admin.site.register(models.Pearl)
admin.site.register(models.MetalType)
admin.site.register(models.JewelleryType)
admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.ReviewProduct, ReviewProductAdmin)
