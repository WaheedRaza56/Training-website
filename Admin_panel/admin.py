from django.contrib import admin
from .models import Product, ProductDetail, Order, OrderDetail, Customer, Cart, Checkout, Category, ProductCategory,CategoryImage,wishlist

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'stock', 'price', 'category','orders', 'rating')
    search_fields = ('product',)
    list_filter = ('rating','id',)
    ordering = ('product',)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product','id', 'size', 'color', 'revenue')
    search_fields = ('product__product',)
    list_filter = ('size', 'color')
    ordering = ('product', 'size', 'color')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'id','product', 'order_date', 'amount', 'payment_method', 'delivery_status')
    search_fields = ('customer', 'product__product')
    list_filter = ('payment_method', 'delivery_status')
    ordering = ('-order_date',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id','order', 'product_detail', 'quantity', 'total_amount', 'rating')
    search_fields = ('order__customer', 'product_detail__product__product')
    list_filter = ('rating',)
    ordering = ('order', 'product_detail')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'email', 'phone', 'joining_date')
    search_fields = ('customer', 'email')
    list_filter = ('joining_date',)
    ordering = ('-joining_date',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'order_detail')
    search_fields = ('customer__customer',)
    ordering = ('customer',)

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'first_name', 'last_name', 'email', 'phone', 'address', 'country', 'state', 'zipcode')
    search_fields = ('customer__customer', 'email')
    ordering = ('customer',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ('id','image','category','title',)
    ordering = ('id',)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'category')
    search_fields = ('product__product', 'category__name')
    ordering = ('product', 'category')

class wishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product','quantity','date',)
    search_fields = ('user',)
    ordering = ( 'date',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(wishlist, wishlistAdmin)
