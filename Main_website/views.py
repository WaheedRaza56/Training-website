from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.template.loader import render_to_string
from django.core import serializers



import logging
from .models import *




class BaseViewMixin(object):
    def get_common_context(self):
        common_context = {
            # 'categories' : Category.objects.prefetch_related('images').all(),
            'product' : Product.objects.all(),
            'Categoryimage' : CategoryImage.objects.all(),
            'Productdetail' : ProductDetail.objects.all(),
            'Customers' : Customer.objects.all(),
            'Orders' : Order.objects.all(),
            'Orderdetail' : OrderDetail.objects.all(),
            'Carts' : Cart.objects.all(),
            'Checkouts' : Checkout.objects.all(),
            'ProductCategories' : ProductCategory.objects.all(),
            'wishlists' : wishlist.objects.all(),
        }
        return common_context
    
    
class BaseView(BaseViewMixin, View):
    template_name = 'enroll/base.html'

# ==================================================   Sign_in    ==================================================




logger = logging.getLogger(__name__)

def signin(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'redirect_url': 'home'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
        except Exception as e:
            logger.error("Error during signin: %s", str(e))
            return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'})

    return render(request, 'enroll/practice.html')


##########################################     sign_up     ########################



def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        username = request.POST.get('Username')  
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        return JsonResponse({'status': 'success', 'redirect_url': '/main-web/'})

    return render(request, 'enroll/practice.html')



##########################################     home     ########################

def home(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    

    
    context = {
        
        **common_context,
        'categories' : Category.objects.prefetch_related('images').all(),

    }
    return render(request, 'enroll/home.html', context )


##########################################    addtowishlist   ########################

# @login_required(login_url='signin')



def addtowishlist(request):
    item_id = request.GET.get('id')
    print('item_id :',item_id)

    if item_id is None:
        return JsonResponse({"error": "Invalid item ID"}, status=400)

    try:
        product = Product.objects.get(id=item_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product does not exist"}, status=404)

    print("product:", product)

    wishlist_count = wishlist.objects.filter(product=product, user=request.user).count()
    product_in_wishlist = wishlist.objects.filter(product=product, user=request.user).exists()


    if product_in_wishlist:
        context = {
            "bool": True,
            "wishlist_count": wishlist_count
        }
    else:
        wishlist.objects.create(product=product, user=request.user)
        context = {
            "bool": True,
            "wishlist_count": wishlist_count + 1
        }
        
        print('wishlist_count :',wishlist_count )

    return JsonResponse(context)

   
   
##########################################   deletefromwishlist   ########################

@login_required(login_url='signin')

def deletefromwishlist(request):
    if request.method == "POST":
        print("POST request received")
        pid = request.POST.get('id')
        print("Received ID:", pid)

        wishlist_item = get_object_or_404(wishlist, id=pid, user=request.user)
        wishlist_item.delete()

        # Fetch updated wishlist items
        updated_wishlist = wishlist.objects.filter(user=request.user)
        context = {
            "wishlists": updated_wishlist,
        }
        data = render_to_string("enroll/practice.html", context)
        print("Data rendered successfully")

        return JsonResponse({"data": data})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
##########################################   addtocart   ########################

# @login_required(login_url='signin')

# def addtocart(request):
#     return render(request, 'enroll/cart.html')

##########################################    search    ########################

# @login_required(login_url='signin')

# def search(request):
#     return render(request, 'enroll/search.html')

##########################################   shop  ########################

@login_required(login_url='signin')

def shop(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/shop.html',context)


##########################################    product   ########################

@login_required(login_url='signin')

def product(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/product.html',context)


##########################################   contact   ########################

@login_required(login_url='signin')

def contact(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/contact.html',context)


