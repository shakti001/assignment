
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homePage, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/',views.login , name="login"),
    path('logout/',views.logout , name="logout"),

    
    path('product-details/<slug>', views.productDetails, name="productDetails"),
    path('add-cart/' ,views.addToCart, name="addTocart"),
    path('cart/' , views.cart, name="cart"),
    path('remove-cart/<slug>/' , views.removeCartItems, name="removeCartItems")



]
