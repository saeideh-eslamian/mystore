from django.shortcuts import render, get_object_or_404, redirect
from . models import *
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, ShippingAddressForm


def store(request):
    products = Product.objects.all().order_by('-update_date')

    if request.method == "POST": 
        if request.user.is_authenticated:   
            customer= request.user.customer
            order, created = Order.objects.get_or_create(customer=customer)
            order_items = order.orderitem_set.all()
            product_id = request.POST['product_id']
            product = Product.objects.get(id = product_id)
            if order_items.filter(product=product, order=order).exists():
                order_item = OrderItem.objects.get(product=product, order=order)
                order_item.quantity += 1
                order_item.save()
            else:
                order_item = OrderItem.objects.create(product=product, quantity=1, order = order)           

                return redirect(request.path)
        else:
          return redirect("login")    

    context = {
        "products" : products,
    }

    return render(request, "store/store.html", context)

def product(request, id):
    product = get_object_or_404(Product, pk = id)

    context = {
        "product" : product,
    }
    return render(request, "store/product.html", context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        order_items = order.orderitem_set.all()

    else:
         order_items = []
         order = {"total_price" : 0,}
     
    if request.method == "POST":
        id_product = request.POST["product_id"] 
        order_item = order_items.get(id = id_product)
        if request.POST["change_quantity"] == "minus":
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()

        if request.POST["change_quantity"] == "plus":
                order_item.quantity += 1
                order_item.save()  
            
    context = {
        "order_items" : order_items,
        "order" : order,
    }        
    return render(request, "store/cart.html", context)
     

def payment_page(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        order_items = order.orderitem_set.all()
        shippin_address , created = ShippinAddress.objects.get_or_create(customer=customer)

        is_address = False
        if created:
            print("yessssssssssssssssss")
            is_address == True
            context = {
            "order_items" : order_items,
            "order" : order,
            "shippin_address": shippin_address,
            }

        else:
            print("nooooooooooooooo")
            is_address == False
            if request.method == "POST":
                address_form = ShippingAddressForm(request.POST)
                if address_form.is_valid():
                    address_form.save()
                else:
                     address_form = ShippingAddressForm()   
                context = {
                "order_items" : order_items,
                "order" : order,
                "address_form": address_form,
                } 
            else:
                address_form = ShippingAddressForm()
                context = {
                "order_items" : order_items,
                "order" : order,
                "address_form": address_form,
                } 
                
               
    else:
        context = {}
        return redirect("login")
    
    
    return render(request, "store/payment.html",context)   

def login_view(request):

    is_login = True

    if request.method == "POST":
        email = request.POST["email"]   
        password = request.POST["password"] 
        user = authenticate(request, username=email, email=email, password=password )
        print(user)
        if user is not None:
            login(request, user)
            return redirect("store")
        
        else:
            is_login = False
            error_message = 'Invalid username or password'
            print(is_login)
        context = {
            "is_login": is_login ,
            "error_message":error_message,
        }
        return render(request, "store/login.html",context)
    else:
        return render(request, "store/login.html")

def logout_view(request):
    logout(request)
    return redirect("store")

def register_view(request):
    is_register= True
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email):
                form = RegisterForm(request.POST)
                is_register= False
                error_message = 'This email already register' 
                context={
                    "is_register": is_register ,
                    "error_message":error_message,
                      "form": form,
                } 
                return render(request, "store/register.html",context)

            else:
                user = User.objects.create(username = email, first_name=first_name,
                                            last_name=last_name,email=email)
                user.set_password(password)
                user.save()
                Customer.objects.create(user=user)
                return redirect("store")
  
    else:       
        form = RegisterForm()
        return render(request, "store/register.html",{"form": form})
    
