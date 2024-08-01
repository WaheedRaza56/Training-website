import logging
from .models import *
from decimal import Decimal
from django.views import View
from django.db.models import Q
from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import authenticate , login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required





##########################################   BaseViewMixin   ############################



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
    
    
    
##########################################     sign_up    ############################### 


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


##########################################   Sign_in   ##################################



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







##########################################     home     #################################


def home(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    

    
    context = {
        
        **common_context,
        'categories' : Category.objects.prefetch_related('images').all(),

    }
    return render(request, 'enroll/home.html', context )


##########################################    addtowishlist   ###########################


@login_required(login_url='signin')

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

    print('wishlist count is ',wishlist_count)

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
        
        
    total_wishlist_count = wishlist.objects.filter(user=request.user).count()
    context["total_wishlist_count"] = total_wishlist_count
    
    print('total wishlist',total_wishlist_count)

    return JsonResponse(context)

   
   
##########################################   deletefromwishlist   #######################


def deletefromwishlist(request):
    if request.method == "POST":
        print("POST request received")
        pid = request.POST.get('id')
        print("Received ID:", pid)

        wishlist_item = get_object_or_404(wishlist, id=pid, user=request.user)
        wishlist_item.delete()

        updated_wishlist = wishlist.objects.filter(user=request.user)
        context = {
            "wishlists": updated_wishlist,
        }
        data = render_to_string("enroll/practice.html", context)
        print("Data rendered successfully")

        return JsonResponse({"data": data})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    
    
##########################################   addtocart   ################################



@login_required(login_url='signin')
def addtocart(request):
    product_id = request.GET.get('id')
    item_quantity = request.GET.get('item_quantity')
    
    print('product id ',product_id)
    print('item quantity ',item_quantity)
    

    context = {"bool": False} 

    if product_id and item_quantity:
        try:
            product_id = int(product_id)
            item_quantity = int(item_quantity)

            product = get_object_or_404(Product, id=product_id)
            print('product ',product)
            customer = get_object_or_404(Customer)
            print('customer',customer)
            
            product_details = ProductDetail.objects.filter(product=product)
            if not product_details.exists():
                product_detail = ProductDetail.objects.create(product=product, size='M', color='BL', revenue=3)
                print('Created ProductDetail:', product_detail)
            else:
                product_detail = product_details.first()
                print('Found ProductDetail:', product_detail)
                
                
            cart_items = Cart.objects.filter(customer=customer, order_detail__product_detail__product=product)
            print('cart-item',cart_items)
            
            if cart_items.exists():
                cart_item = cart_items.first()
                print('cart-item',cart_item)
                cart_item.quantity += item_quantity
                cart_item.save()
                context = {'bool': True, 'cart_quantity': cart_item.quantity}
            else:
                order_detail = OrderDetail.objects.create(
                    order=Order.objects.create(customer=customer, product=product),
                    product_detail=ProductDetail.objects.get(product=product),  
                    quantity=item_quantity,
                    total_amount=product.price * item_quantity
                )
                cart_item = Cart.objects.create(customer=customer, order_detail=order_detail, quantity=item_quantity)
                cart_item.save()
                wishlist.objects.filter(user=request.user, product=product).delete()
                context = {"bool": True, "cart_item": cart_item.quantity}
                
            total_cart_items = Cart.objects.filter(customer=customer).count()
            context['total_cart_items'] = total_cart_items
            
            total_wishlist_count = wishlist.objects.filter(user=request.user).count()
            context['total_wishlist_count'] = total_wishlist_count
            
            print('total cart item ', total_cart_items)
            

        except (ObjectDoesNotExist, ValueError) as e:
            context = {"bool": False, "text": str(e)}

    return JsonResponse(context)


##########################################    deletefromcart    ########################


def deletefromcart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('id')
        print('cart_id', cart_id)
        
        try:
            customer = get_object_or_404(Customer)
            delete_from_cart = get_object_or_404(Cart, id=cart_id, customer=customer) 
            delete_from_cart.delete()
            
            total_cart_items = Cart.objects.filter(customer=customer).count()
            
            context = { 
                'total_cart_items': total_cart_items,
                'message': 'Item successfully removed from cart'
            }
        except Cart.DoesNotExist:
            context = { 
                'total_cart_items': Cart.objects.filter(customer=customer).count(),
                'message': 'Item not found in cart'
            }
        
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    

##########################################    cart_price    #############################


def cart_price(request):
    customer = get_object_or_404(Customer)
    carts = Cart.objects.filter(customer=customer)
    amount = sum( item.price()  for item in carts )
    shipping_charges = Decimal('90.0')
    total_amount = amount + shipping_charges
    
    context = {
        'amount':amount,
        'total_amount':total_amount,
    }
    return JsonResponse(context)




##########################################    plus_cart    #################################


def plus_cart(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        customer = get_object_or_404(Customer)
        cart_item = get_object_or_404(Cart, order_detail__product_detail__product=id, customer=customer)
        
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
        cart_item.refresh_from_db()  
        
        cart_items = Cart.objects.filter(customer=customer)
        shipping_charges = Decimal('90.0')
        total_amount = sum(item.total_price() for item in cart_items) + shipping_charges
        
        return JsonResponse({
            'quantity': cart_item.quantity,
            'amount': cart_item.total_price(),
            'total_amount': total_amount
        })





##########################################    minus_cart    #################################


def minus_cart(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        customer = get_object_or_404(Customer)
        cart_item = get_object_or_404(Cart, order_detail__product_detail__product=id, customer=customer)
        
        if cart_item.quantity > 1:
            cart_item.quantity = F('quantity') - 1
            cart_item.save()
            cart_item.refresh_from_db()  
            
            cart_items = Cart.objects.filter(customer=customer)
            shipping_charges = Decimal('90.0')
            total_amount = sum(item.total_price() for item in cart_items) + shipping_charges
            
            
            return JsonResponse({
                'quantity': cart_item.quantity,
                'amount': cart_item.total_price(),
                'total_amount': total_amount
            })
        else:
            return JsonResponse({'error': 'Quantity cannot be less than 1'}, status=400)
        
        

##########################################   checkout  ######################################


def checkout(request):
    customer = get_object_or_404(Customer)

    if request.method == 'POST':
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        order_note = request.POST.get('order_note')

        if not email or not fname or not lname or not country or not address or not zipcode or not phone:
            return JsonResponse({'status': 'error', 'message': 'All fields marked with * are required'}, status=400)

        if Checkout.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'}, status=400)

        checkout_entry = Checkout(email=email, first_name=fname,last_name=lname,country=country,address=address,zipcode=zipcode,phone=phone,order_note=order_note,customer=customer)
        
        checkout_entry.save()

        carts = Cart.objects.filter(customer=customer)
        for cart in carts:
            cart.checkout = checkout_entry
            cart.save()

    carts = Cart.objects.filter(customer=customer)
    context = {
        'Carts': carts
    }

    return render(request, 'enroll/checkout.html', context)


##########################################   search  ######################################




def search(request):
    query = request.GET.get('q')            
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(product__icontains=query)

    if category and category != 'All Categories':
        products = products.filter(category__name__icontains=category)

    products = products.order_by('price')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = []
        for product in products:
            products_data.append({
                'product': product.product,
                'price': product.price,
                'image': {
                    'url': product.image.url if product.image else ''
                }
            })
        return JsonResponse({'products': products_data})

    context = {
        'products': products,
    }
    return render(request, 'enroll/practice.html', context)



    


##########################################   shop  ######################################

@login_required(login_url='signin')

def shop(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/shop.html',context)


##########################################    product   #################################

@login_required(login_url='signin')

def product(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/product.html',context)


##########################################   contact   ##################################

@login_required(login_url='signin')

def contact(request):
    base_view_mixin = BaseViewMixin() 
    common_context = base_view_mixin.get_common_context() 
    
    context = {
            **common_context,
    }
    return render(request, 'enroll/contact.html',context)


