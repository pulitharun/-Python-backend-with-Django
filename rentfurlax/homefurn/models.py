# models.py

from django.db import models

# Customer model with fields for storing customer information
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    username = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(null=True, max_length=100)

    def __str__(self):  # string representation for the Customer model
        return f"{self.first_name} {self.last_name}"

# Category model for storing different categories of products
class Category(models.Model):
    category_type = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(max_length=100, unique=True , null=True)

    def __str__(self):  # string representation for the Category model
        return self.category_type

# Product model for storing details of rental products
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    delivery_in_days = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    image_url = models.URLField()
    rentaloptions= models.JSONField() 
    

    def __str__(self):   # string representation for the Product model
        return self.name

# Invoice model for storing invoice information
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status= models.CharField(max_length=50, choices=[
        ('ORDERED','Ordered'),
        ('CANCELLED', 'Cancelled'),
        ('DELIVERED', 'Delivered'),
    ])  

    def __str__(self):   # string representation for the Invoice model
        return f"Invoice for {self.product.name} - {self.status}"
