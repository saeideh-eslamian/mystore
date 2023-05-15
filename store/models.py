from django.db import models
from django.contrib.auth.models import User 

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    comment_text = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username}  {self.comment_date}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    descriptin = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to = "images")

    def __str__(self):
        return self.name
    
class ShippinAddress(models.Model):
    address = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    costomer = models.ForeignKey(Customer, on_delete=models.CASCADE)   

    def __str__(self):
        return self.address 


class Order(models.Model):
    customer = models.ForeignKey(Customer,null=True,blank=False,
                                  on_delete=models.SET_NULL)
    date_order = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippinAddress, null=True,
                                          on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.customer.user.username}  {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.OneToOneField(Product,null=True, blank=False,
                                    on_delete=models.SET_NULL)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} : {self.quantity}"

