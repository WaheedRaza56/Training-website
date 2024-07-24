from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as auth_logout, login 
from django.contrib.auth.decorators import user_passes_test
from .forms import LoginForm 
from django.contrib.auth import authenticate, login
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

def is_admin(user):
    return user.is_staff

##########################################_Login_########################################

@user_passes_test(is_admin)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        print("form is not valid")
        if form.is_valid():
            print("form is valid")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('dashboard') 
            else:
                # return redirect('error_404')
                form.add_error(None, 'Invalid username or password.') 
        else:
            form.add_error(None, 'Please correct the errors below.') 
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})
##########################################_logout_#######################################

@user_passes_test(is_admin)
def logout_view(request):
    auth_logout(request)
    return redirect('login')


##########################################error_404########################

@user_passes_test(is_admin)
def error_404(request):
    return render(request, 'account/404_error.html')

##########################################dashboard########################


@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'panel/dashboard.html')

##########################################gallery########################


@user_passes_test(is_admin)
def gallery(request):
    gallery = Category.objects.all()
    
    context = {
        'gallery':gallery,
    }
    
    return render(request, 'panel/gallery.html',context)




##########################################tablelist########################


@user_passes_test(is_admin)
def products(request):
    products = Product.objects.all()
    return render(request, 'panel/products.html',{'products':products})

##########################################save_product_from_request########################

def save_product_from_request(request, product=None):
    product_data = {
        'product': request.POST.get('product'),
        'stock': request.POST.get('stock'),
        'price': request.POST.get('price'),
        'orders': request.POST.get('orders'),
        'manufacturer_name': request.POST.get('manufacturer_name'),
        'manufacturer_brand': request.POST.get('manufacturer_brand'),
        'discount': request.POST.get('discount'),
        'category': Category.objects.get(id=request.POST.get('category')),
        'category_id': request.POST.get('category'),
        'gallery': request.FILES.getlist('gallery') if 'gallery' in request.FILES else None,
        'image': request.FILES.get('image') if 'image' in request.FILES else None,
        'meta_title': request.POST.get('meta_title'),
        'meta_keywords': request.POST.get('meta_keywords'),
        'meta_description': request.POST.get('meta_description'),
    }
 
    
    if product is None:
        product = Product(**product_data)
    else:
        for key, value in product_data.items():
            setattr(product, key, value)
    
    product.save()
    
    if 'gallery' in request.FILES:
        for file in request.FILES.getlist('gallery'):
            product.gallery.save(file.name, file)
    
    return product

##########################################create_product########################


@user_passes_test(is_admin)
def create_product(request):
    if request.method == 'POST':
        save_product_from_request(request)
        return redirect('products')

    categories = Category.objects.all()
    return render(request, 'panel/create_product.html', {'categories': categories})

##########################################edit_product########################


@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        save_product_from_request(request, product)
        return redirect('products')
    
    categories = Category.objects.all()
    return render(request, 'panel/create_product.html', {'product': product, 'categories': categories})

##########################################delete_product########################


@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('products')


##########################################view_product########################


@user_passes_test(is_admin)
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    return render(request, 'panel/create_product.html', {'product': product, 'categories': categories})


##########################################orders########################


@user_passes_test(is_admin)
def orders(request):
    orders = Order.objects.all()
    return render(request, 'panel/orders.html',{'orders':orders})


##########################################product_detail########################


@user_passes_test(is_admin)
def product_detail(request, product_detail_id):
    product_details = ProductDetail.objects.all()
    
    product_detail = get_object_or_404(ProductDetail, id=product_detail_id)
    
    details_with_customers_and_dates = []
    for detail in product_details:
        customers = detail.get_customer()
        order_dates = detail.get_orderdate()
        details_with_customers_and_dates.append({
            'detail': detail,
            'customers': customers,
            'order_dates': order_dates,
        })
    
    context = {
        'details_with_customers_and_dates': details_with_customers_and_dates,
    }

    return render(request, 'panel/product_detail.html', context)




##########################################orders_detail########################


@user_passes_test(is_admin)
def orders_detail(request):
    orders_details = OrderDetail.objects.all()
    
    context = {
        'orders_details': orders_details,
    }
    return render(request, 'panel/orders_detail.html',context)


##########################################customers########################


@user_passes_test(is_admin)
def customers(request):
    customers = Customer.objects.all()
    
    context = {
        'customers': customers,
    }
    return render(request, 'panel/customers.html',context)




##########################################edit_customer########################


# @user_passes_test(is_admin)
# def edit_customer(request, customer_id):
#     if request.method == 'POST':
#         customer = get_object_or_404(Customer, id=customer_id)
#         customer_name = request.POST.get('customer_name')
#         customer_email = request.POST.get('customer_email')
#         customer_phone = request.POST.get('customer_phone')
#         customer_date = request.POST.get('customer_date')
#         customer_status = request.POST.get('customer_status')

#         customer.customer = customer_name
#         customer.email = customer_email
#         customer.phone = customer_phone
#         customer.joining_date = customer_date
#         customer.status = customer_status
#         customer.save()

#         response_data = {
#             'success': True,
#             'customer': {
#                 'customer': customer.customer,
#                 'email': customer.email,
#                 'phone': customer.phone,
#                 'joining_date': customer.joining_date,
#                 'status': customer.status,
#             }
#         }
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'success': False})

##########################################carts########################

