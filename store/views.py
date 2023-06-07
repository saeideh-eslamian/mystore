from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from . models import *
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, ShippingAddressForm
from django.db.models import Q


def store(request):
    products = Product.objects.all().order_by('-update_date')

    if request.method == "POST": 
        if "add_to_cart_submit" in request.POST:
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
                product_id = request.POST['product_id']
                product = Product.objects.get(id = product_id)
                request.session["product_id"] = product_id
                cart = request.session.get('cart', {})
                cart[product_id] = cart.get(product_id,0)+1
                # product = Product.objects.get(id = product_id)
                # if order_items.filter(product=product).exists():
                #     order_item = OrderItem.objects.get(product=product, order=order)
                #     order_item.quantity += 1
                #     order_item.save()
                # else:
                #     order_item = OrderItem.objects.create(product=product, quantity=1) 
                request.session['cart']= cart
                return redirect(request.path)  
              
        elif "submit_search" in request.POST:
            search = request.POST["search"]
            search_result = Product.objects.filter(
                Q(name__icontains=search) | Q(descriptin__icontains=search)
                ).order_by("update_date")
            return render(request,"store/search.html",{"search_result":search_result})


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
        is_user_login = True

    else:
        cart = request.session.get('cart', {}) 
        is_user_login = False
        items = []
        order = {'total_price':0}
        total_price = 0
        for product_id, quantity in cart.items() :
            product = Product.objects.get(id = product_id)
            total =quantity*product.price
            order['total_price'] += total
            item = {
				'id':product.id,
				'product':{
					'id':product.id,
					'name':product.name, 
					'price':product.price, 
				        'imageUrl':product.imageUrl
					}, 
				'quantity':quantity,
				'digital':product.digital,
				'total_price_item':total,
            }
            items.append(item)
        order_items = items

    context = {
        "order_items" : order_items,
        "order" : order,
        "is_user_login" : is_user_login,
    }        
    return render(request, "store/cart.html", context)
     
def payment_page(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        order_items = order.orderitem_set.all()
        is_saved_customer = False
        if ShippinAddress.objects.filter(customer=customer).exists():
            saved_customer_address =ShippinAddress.objects.filter(customer=customer)
            is_saved_customer = True
        else:
            is_saved_customer = False
            saved_customer_address = ""

        if request.method == 'POST':
            if "addressform_submit" in request.POST:
                address_form = ShippingAddressForm(request.POST)
                if address_form.is_valid():
                    is_created_address = False
                    if ShippinAddress.objects.filter(customer=customer,
                        address=address_form.cleaned_data['address'],
                        city=address_form.cleaned_data['city'],
                        state=address_form.cleaned_data['state'],
                        zipcode=address_form.cleaned_data['zipcode'],
                        phone_number=address_form.cleaned_data['phone_number']).exists():

                        is_created_address = True
                        massage = "This address already exist"
                    if not is_created_address:
                        address =ShippinAddress.objects.create(
                            customer=customer,
                            address=address_form.cleaned_data['address'],
                            city=address_form.cleaned_data['city'],
                            state=address_form.cleaned_data['state'],
                            zipcode=address_form.cleaned_data['zipcode'],
                            phone_number=address_form.cleaned_data['phone_number'],
                            )
                        order.shipping_address = address
                        
                        massage = "your address saved successful"
                        return redirect("payment")
                else:
                        address_form = ShippingAddressForm(request.POST)
                        massage = "Please inter valid information"  
                context = {
                "order_items" : order_items,
                "order" : order,
                "address_form": address_form,
                "massage": massage,
                "saved_customer_address": saved_customer_address,
                "is_saved_customer": is_saved_customer,
                } 
                return render(request, "store/payment.html",context)
            
            elif "select_address_submit" in request.POST:
                select_address = request.POST.get("select_address")
                selected_address = ShippinAddress.objects.get(address=select_address)
                data = {
                'address': selected_address.address,
                'city': selected_address.city,
                'phone_number':selected_address.phone_number,
                'zipcode': selected_address.zipcode,
                'state': selected_address.state,
                'customer': selected_address.customer,
                     }
                
                fill_form_by_select_address = ShippingAddressForm(initial=data)
                
                context = {
                "order_items" : order_items,
                "order" : order,
                "address_form": fill_form_by_select_address,
                "saved_customer_address": saved_customer_address,
                "is_saved_customer": is_saved_customer,
                } 
                return render(request, "store/payment.html",context)



            
        address_form = ShippingAddressForm()
        context = {
        "order_items" : order_items,
        "order" : order,
        "address_form": address_form,
        "saved_customer_address": saved_customer_address,
        "is_saved_customer": is_saved_customer,
        } 
        return render(request, "store/payment.html",context)


    else:
        context = {}
        return redirect("login")
    
       

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
    
