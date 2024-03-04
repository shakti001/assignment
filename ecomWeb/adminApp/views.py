from django.shortcuts import render,redirect
from ecomWebApp.models import *
from django.contrib.auth import authenticate, login as login_check
from django.contrib import messages
from django.contrib.auth.models import User, auth
# from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from ecomWebApp.helpers import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import MD5PasswordHasher, make_password
from django.contrib.contenttypes.models import ContentType   
from django.contrib.auth.models import Group, Permission
import calendar
from collections import Counter

# User = get_user_model()

# Create your views here.
@login_required(login_url="/admin")

def home(request):
    try:
        user = User.objects.filter(is_superuser = False).count()
        product = Product.objects.all().count()
        return render(request,"admin/home/index.html", {'product':product, 'user':user })
    except:
        messages.error(request, "Something went wrong")
        return render(request,"admin/home/index.html")


def login(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(email=email).exists():
                user = auth.authenticate(email=email, password=password)
                if user is None:
                    messages.error(request, "Invalid email & passsword")
                    return redirect('/admin')
                elif user.is_superuser == True:
                    messages.success(request, "Welcome in Adminpanel")

                    auth.login(request, user)
                    return redirect("/admin/home/")
                elif user.roll == "Subadmin":
                    auth.login(request, user)
                    return redirect("/admin/home/")

                else:
                    messages.error(request, "Invalid email & passsword")
                    return redirect('/admin')
            else:
                messages.error(request, "Invalid email & passsword")
                return redirect('/admin')
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/')
    return render(request,"admin/auth/login.html")

def forgotPassword(request):
    try:
        if request.method=="POST":
            email = request.POST.get("email")
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_superuser == True:
                    otp = generateOTP()
                    user.Otp = otp
                    user.save()
                    # send_to = [email]
                    # subject = "ONE TIME PASSOWRD"
                    # content = (
                    #     "Hi Superadmin "
                    #     + "Your ONE TIME PASSWORD is"
                    #     + otp
                    # )
                    # sendMail(subject, content, send_to)
                    messages.success(request,"Please Enter Otp Here.")
                    return redirect("/admin/otp-verify/"+str(user.slug))                
                else:
                    messages.error(request, "Email not found !!!")
                    return redirect('/admin/forgot-password/')
            else:
                messages.error(request, "Email not found !!!")
                return redirect('/admin/forgot-password/')
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/forgot-password/')
    return render(request,"admin/auth/forgotpassword.html")

def otp_verify(request, slug):
    try:
        if request.method == "POST":
            otp = request.POST.get('otp')
            user = User.objects.get(slug=slug)
            if otp:
                if otp == user.Otp:
                    user.Otp = ""
                    user.save()
                    messages.success(request, "Please enter new password !!!")
                    return redirect("/admin/forgot-password-form/" + str(user.slug))
                else:
                    messages.error(request, "Otp does not match !!!")
                    return redirect('/admin/otp-verify/'+str(user.slug))
            else:
                messages.error(request, "Please enter Otp  !!!")
                return redirect('/admin/otp-verify/'+str(user.slug))
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/otp-verify/'+str(user.slug))   
    return render(request,"admin/auth/otp-verify.html")
    
def forgotPasswordForm(request, slug):
    try:
        if request.method == "POST":
            newpassword = request.POST.get("npassword")
            confirmnewpassword = request.POST.get("cnpassword")
            user = User.objects.get(slug=slug)
            if newpassword and confirmnewpassword:
                if newpassword == confirmnewpassword:
                    user.password = make_password(newpassword)
                    user.save()
                    messages.success(request, "Password changed Successfully !!!")
                    return redirect("/admin/")
                else:
                    messages.error(request, "Password does not matched !!!")
                    return redirect("/admin/forgot-password-form/" + str(user.slug))
            else:
                messages.error(request, "Please enter Newpassword !!!")
                return redirect("/admin/forgot-password-form/" + str(user.slug))
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect("/admin/forgot-password-form/" + str(user.slug))   
    return render(request,"admin/auth/forgotpasswordform.html")

@login_required(login_url="/admin")
def logout(request):
    auth.logout(request)
    return redirect("/admin/")

@login_required(login_url="/admin")
def change_password(request, slug):
    try:
        if request.method == "POST":
            password = request.POST.get("pass")
            print(password)
            new_passowrd = request.POST.get("newpass")
            rnew_passowrd = request.POST.get("cnewpass")
            user = User.objects.get(slug=slug)

            check = user.check_password(password)
            if check == True:
                if new_passowrd == rnew_passowrd:
                    user.set_password(new_passowrd)
                    user.save()
                    auth.login(request, user)
                    messages.success(request, " Password changed Successfully !!!! ")
                    return redirect("/admin/change-password/" + str(slug))
                else:
                    messages.error(request, " Password Does not Match !!!! ")
                    return redirect("/admin/change-password/" + str(slug))
            else:
                messages.error(request, " Old password Does not Match !!!! ")
                return redirect("/admin/change-password/" + str(slug))
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect("/admin/change-password/" + str(slug))  
    return render(
        request, "admin/profile/change-password.html"
    )

@login_required(login_url="/admin")
def categoryList(request):
    try:
        category = Category.objects.all()
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect("/admin/category/")  
    return render(request,"admin/category/category.html",{'category':category})


@login_required(login_url="/admin")
def add_category(request):
    try:
        if request.method == "POST":
            category_name = request.POST.get('category_name')
            parent_id = request.POST.get('sub_category')
            if category_name is not None:
                if parent_id is not None:
                    data = Category.objects.create(name=category_name,parent_id=parent_id)
                    return JsonResponse({'status':'success', 'message':'category create successfully'})
                else:
                    data = Category.objects.create(name=category_name)
                    return JsonResponse({'status':'success', 'message':'category create successfully'})
            else:
                messages.error(request, "Fill all fileds !!")
                return redirect('/admin/add-category/')
        category = Category.objects.filter(parent_id__isnull=True)
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect("/admin/add-category/")        
    return render(request, "admin/category/add_category.html",{'category':category})

@login_required(login_url="/admin")
def edit_category(request,slug):
    try:
        subCategory = Category.objects.get(slug=slug)
        category = Category.objects.filter(parent_id__isnull=True)        
        if request.method == "POST":
            category_name = request.POST.get('name')
            parent_id = request.POST.get('category_id')
            if category_name is not None:
                if parent_id is not None:
                    data = Category.objects.get(slug=slug)
                    data.name= category_name
                    data.parent_id= parent_id
                    data.save()
                    return JsonResponse({'status':'success', 'message':'category update successfully'})
                else:
                    data = Category.objects.get(slug=slug)
                    data.name= category_name
                    data.save()
                    return JsonResponse({'status':'success', 'message':'category update successfully'})
            else:
                messages.error(request, "Fill all fileds !!")
                return redirect('/admin/edit-category/'+str(slug))
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/edit-category/'+str(slug))   
    return render(request, "admin/category/edit-category.html",{'subCategory':subCategory,'category':category})

@login_required(login_url="/admin")
def delete_category(request, slug):
    data = Category.objects.get(slug=slug)
    data.delete()
    messages.success(request,"Category deleted successfully  !!!!!")
    return redirect("/admin/category/")

@login_required(login_url="/admin")
def tags(request):
    tags = Tags.objects.all()
    return render(request, "admin/tags/tags.html", {'tags':tags})

@login_required(login_url="/admin")
def add_tags(request):
    try:
        if request.method == "POST":
            name = request.POST.get('tag_name')
            data = Tags.objects.create(name=name)
            messages.success(request, "Product Tags created succssfully !!!")
            return redirect('/admin/add-tags/')
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/add-tags/')   
    return render(request, "admin/tags/add_tags.html")

@login_required(login_url="/admin")
def edit_tags(request,slug):
    try:
        data = Tags.objects.get(slug=slug)
        if request.method == "POST":
            name = request.POST.get('tag_name')
            data.name = name
            data.save()
            messages.success(request, "Product Tags updated succssfully !!!")
            return redirect('/admin/edit-tags/'+str(slug))
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/edit-tags/'+str(slug))  
    return render(request, "admin/tags/edit_tags.html",{'data':data})

@login_required(login_url="/admin")
def delete_tags(request,slug):
    data = Tags.objects.get(slug=slug)
    data.delete()
    messages.success(request, "Product Tags deleted succssfully !!!")
    return redirect('/admin/tags')

@login_required(login_url="/admin")
def product(request):
    product = Product.objects.all()
    return render(request, "admin/product/product.html",{'product':product})

@login_required(login_url="/admin")
def add_product(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            image = request.FILES.get('image')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            tags = request.POST.getlist('tags')
            if name and category and image and stock and price:
                data = Product.objects.create(category_id = category, name=name,image=image,stock=stock,price=price)
                if data:
                    for tag in tags:
                        tag_data = ProductTags.objects.create()
                        tag_data.tags.add(*tag)
                        tag_data.product.add(data.id)
                        return JsonResponse({'status':'success', 'message':"Product created successfully !!! "})
                else:
                    return JsonResponse({'status':'error', 'message':"error accourd !!! "})
            else:
                return JsonResponse({'status':'error', 'message':"All fileds required !!! "})
        tags = Tags.objects.all()
        category = Category.objects.filter(parent_id__isnull=True)        
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/add-product/')  

    return render(request, "admin/product/add_product.html",{'tags':tags,'category':category})

@login_required(login_url="/admin")
def edit_product(request,slug):
    try:
        data = Product.objects.get(slug=slug)
        if request.method == "POST":
            name = request.POST.get('name')
            image = request.FILES.get('image')
            category = request.POST.get('category')

            
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            tags = request.POST.getlist('tags')
            if name and category and  image and stock and price:
                    data.name = name
                    data.category_id= category
                    data.image = image
                    data.stock = stock
                    data.price = price
                    data.save()
                    if data:
                        tag_data = ProductTags.objects.all()
                        tag_data.filter(product = data.id)
                        tag_data.delete()
                        for tag in tags:
                            tag_data = ProductTags.objects.create()
                            tag_data.tags.add(*tag)
                            tag_data.product.add(data.id)
                        return JsonResponse({'status':'success', 'message':"Product updated successfully !!! "})
                    else:
                        return JsonResponse({'status':'error', 'message':"error accourd !!! "})
            else:
                return JsonResponse({'status':'error', 'message':"All fileds required !!! "})
        tags = Tags.objects.all()
        tag_data = ProductTags.objects.filter(product=data.id)
        category = Category.objects.filter(parent_id__isnull=True)
    except:
        messages.error(request, "Someting went wrong !!!")
        return redirect('/admin/edit-product/'+str(slug))        

    return render(request, "admin/product/edit-product.html",{'tags':tags,'data':data,'category':category, 'tag_data':tag_data})
     
@login_required(login_url="/admin")
def delete_product(request,slug):
    data = Product.objects.get(slug=slug)
    data.delete()
    messages.success(request, "Product is deleted")
    return redirect('/admin/delete-product/'+str(slug))