from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')

    def __str__(self):
        return self.name or ''
    


class Product(models.Model):
    product = models.CharField(max_length=150, unique=True , null=True)
    stock = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    orders = models.PositiveIntegerField(default=1)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    description = models.TextField(default='')
    manufacturer_name = models.CharField(max_length=100, default='')
    manufacturer_brand = models.CharField(max_length=100, default='')
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    gallery = models.FileField(upload_to='images/', null=True, blank=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product or ''

    def get_available_sizes(self):
        return list(self.productdetail_set.values_list('size', flat=True).distinct())

    def get_available_colors(self):
        return list(self.productdetail_set.values_list('color', flat=True).distinct())

class CategoryImage(models.Model):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
    ]

    BLUE = 'BL'
    GREEN = 'GR'
    RED = 'RD'
    YELLOW = 'YL'
    BLACK = 'BK'
    WHITE = 'WH'
    ORANGE = 'OR'

    COLOR_CHOICES = [
        (BLUE, 'Blue'),
        (GREEN, 'Green'),
        (RED, 'Red'),
        (YELLOW, 'Yellow'),
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (ORANGE, 'Orange'),
    ]
    
    category = models.ForeignKey(Category, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, default='') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) 
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=SMALL)
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, default=BLACK)


    def __str__(self):
        return f"{self.category.name} Image"

class ProductDetail(models.Model):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
    ]

    BLUE = 'BL'
    GREEN = 'GR'
    RED = 'RD'
    YELLOW = 'YL'
    BLACK = 'BK'
    WHITE = 'WH'
    ORANGE = 'OR'

    COLOR_CHOICES = [
        (BLUE, 'Blue'),
        (GREEN, 'Green'),
        (RED, 'Red'),
        (YELLOW, 'Yellow'),
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (ORANGE, 'Orange'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=SMALL)
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, default=BLACK)
    revenue = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f'{self.product.product}'
    
    def get_customer(self):
        orders = OrderDetail.objects.filter(product_detail=self)
        customers = ", ".join(order.order.customer.customer for order in orders)
        return customers


    def get_orderdate(self):
        orders = OrderDetail.objects.filter(product_detail=self)
        order_dates = ", ".join(order.order.order_date.strftime("%Y-%m-%d") for order in orders)
        return order_dates



class Customer(models.Model):
    customer = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=55, default='')
    phone = models.CharField(max_length=15)
    joining_date = models.DateField(default=date.today)

    def __str__(self):
        return self.customer
    

class Order(models.Model):
    MASTERCARD = 'Mastercard'
    VISA = 'Visa'
    PAYPAL = 'PayPal'
    CASH_ON_DELIVERY = 'Cash on Delivery'
    OTHER = 'Other'

    PAYMENT_METHOD_CHOICES = [
        (MASTERCARD, 'Mastercard'),
        (VISA, 'Visa'),
        (PAYPAL, 'PayPal'),
        (CASH_ON_DELIVERY, 'Cash on Delivery'),
        (OTHER, 'Other'),
    ]

    ACTIVE = 'active'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

    DELIVERY_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateField(default=date.today)
    amount = models.PositiveBigIntegerField(default=1)
    payment_method = models.CharField(max_length=55, choices=PAYMENT_METHOD_CHOICES, default=MASTERCARD)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return f'Order for {self.product.product} by {self.customer.customer}'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.PositiveBigIntegerField(default=1)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    def __str__(self):
        return f'{self.order.customer} - {self.product_detail.product.product}'





class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Checkout(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=55, default='')
    last_name = models.CharField(max_length=55, default='')
    email = models.EmailField(max_length=55, default='')
    phone = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=55, default='')
    state = models.CharField(max_length=55, default='')
    zipcode = models.CharField(max_length=10, default='')

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.product} - {self.category.name}'


class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(default=date.today)
    
    def __str__(self):
        return f'{self.product.product} wishlisted by {self.user}'