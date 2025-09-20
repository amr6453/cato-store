from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total_amount', 'created_at', 'total_items')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    inlines = [OrderItemInline]
    actions = ['mark_shipped', 'mark_cancelled']
    readonly_fields = ('created_at',)

    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f"{updated} order(s) marked as shipped.")
    mark_shipped.short_description = 'Mark selected orders as shipped'

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"{updated} order(s) marked as cancelled.")
    mark_cancelled.short_description = 'Mark selected orders as cancelled'

    def total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    total_items.short_description = 'Total items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name',)
