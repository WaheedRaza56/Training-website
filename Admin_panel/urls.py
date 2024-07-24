from django.urls import path
from . import views

urlpatterns = [
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),

    path('error_404/', views.error_404, name='error_404'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('gallery/', views.gallery, name='gallery'),
    path('products/', views.products, name='products'),
    
    path('create_product/', views.create_product, name='create_product'),
    path('product_detail/<int:product_detail_id>/', views.product_detail, name='product_detail'),
    
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('view_product/<int:product_id>/', views.view_product, name='view_product'),
    
    path('orders/', views.orders, name='orders'),
    path('orders_detail/', views.orders_detail, name='orders_detail'),
    path('customers/', views.customers, name='customers'),
]
