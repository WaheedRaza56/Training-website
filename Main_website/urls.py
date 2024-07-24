from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    # path('logout/', views.logoutUser, name='logout'),
    
    
    
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    
    path('add-to-wishlist/',views.addtowishlist,name='addtowishlist'),
    path('deletefromwishlist', views.deletefromwishlist, name='deletefromwishlist'),

    # path('add-to-cart/',views.addtocart,name='addtocart'),

    # path('search/',views.search,name='search'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    