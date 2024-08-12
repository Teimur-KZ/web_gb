from django.contrib import admin
from .models import Category, Product, Brand, ProductSize, ProductSizeQuantity
from django.core.exceptions import ValidationError

@admin.action(description='Сбросить кол. товара на 0')
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)

class ProductSizeQuantityInline(admin.TabularInline):
    model = ProductSizeQuantity
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    actions = [reset_quantity]
    list_display = ('name', 'category', 'brand', 'price', 'delivery_price', 'date_added', 'rating', 'active')
    list_filter = ('category', 'brand', 'date_added', 'rating', 'active', 'delivery_price')
    search_fields = ('name', 'description')
    list_editable = ('price', 'active', 'delivery_price')
    readonly_fields = ['date_added', 'rating']
    fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['name', 'image', 'product_weight', 'delivery_time']
        }),
        ('Категория товара и его подробное описание', {
            'classes': ['collapse'],
            'fields': ['category', 'brand', 'description'],
        }),
        ('Цена', {
            'fields': ['price', 'delivery_price']
        }),
        ('Рейтинг и прочее', {
            'fields': ['date_added', 'rating', 'active'],
        }),
        ('SEO', {
            'fields': ['seo_title', 'seo_description', 'seo_keywords']
        }),
    ]
    inlines = [ProductSizeQuantityInline]

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'category')
    list_editable = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'description', 'seo_title', 'seo_description', 'seo_keywords']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(ProductSize, ProductSizeAdmin)
