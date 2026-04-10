from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    vendor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# --- NEW ORDER MODEL FOR ADMIN TRACKING ---
class Order(models.Model):
    # This links the order to the product and the user who bought it
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    
    # Customer Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    
    # Order Info
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order Status (Viewable/Editable in Admin Panel)
    STATUS_CHOICES = (
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Order {self.id} - {self.product.name} by {self.first_name}'