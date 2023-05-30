from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('payment/', views.payment_page, name="payment"),
    path('login/',views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.register_view,name="register"),
    path('product/<int:id>/', views.product, name="product"),
    
]
