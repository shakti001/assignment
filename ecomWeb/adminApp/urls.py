
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from adminApp import views
from .views import *
urlpatterns = [
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('change-password/<slug>', views.change_password),
    path('forgot-password/', views.forgotPassword),
    path('otp-verify/<slug>/', views.otp_verify),
    path('forgot-password-form/<slug>/', views.forgotPasswordForm),
    path('category/', views.categoryList),
    path('add-category/', views.add_category),
    path('edit-category/<slug>', views.edit_category),
    path('delete-category/<slug>', views.delete_category),
    path('tags/', views.tags),
    path('add-tags/', views.add_tags),
    path('edit-tags/<slug>', views.edit_tags),
    path('delete-tags/<slug>', views.delete_tags),
    path('product/', views.product),
    path('add-product/', views.add_product),
    path('edit-product/<slug>', views.edit_product),
    path('delete-product/<slug>/', views.delete_product),


    

    

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    


    





]
