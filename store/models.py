from django.db import models
from django.contrib.auth.models import User 

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    comment_text = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment_date = models.DateTimeField(null=True,auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username}  {self.comment_date}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    descriptin = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment, null=True,blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to = "images", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def imageUrl(self):
        try:
            url =self.image.url
        except:
            url = ''
        return url        
    
class ShippinAddress(models.Model):
    address = models.CharField(max_length=200, default="")
    phone_number = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(max_length=30,null=True,blank=True)
    city = models.CharField(max_length=30,default="")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)   

    def __str__(self):
        return self.address 


class Order(models.Model):
    customer = models.ForeignKey(Customer,null=True,blank=False,
                                  on_delete=models.SET_NULL)
    date_order = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippinAddress, null=True, blank=True,
                                          on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.customer} : {self.date_order}"


    @property
    def total_price(self):
        # total = 0
        # for item in self.orderitem_set.all():
        #     total += item.total_price_item
        order_items = self.orderitem_set.all()
        total = sum([ item.total_price_item for item in order_items ])

        return total    
                       

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,null=True, blank=False,
                                    on_delete=models.SET_NULL)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} : {self.quantity}"
    
    @property
    def total_price_item(self):
        return(self.quantity * self.product.price)


