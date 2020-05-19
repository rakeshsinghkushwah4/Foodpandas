"""food_pandas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from customer import views
from django.views.generic import RedirectView

urlpatterns = [
  path('dashboard/',views.home,name="user_dashboard"),
  path('store/',views.store,name='store'),
  path('product_detail/<slug:slug>',views.prodcut_detail,name='product_detail'),
  path('more_product/<int:tag>',views.more_product,name='more_product'),
  path('update_item/',views.updateItem,name='update_item'),
  path('cancel_order/',views.cancelOrderItems,name='cancel_order'),
  path('cart/',views.cart,name='cart'),
  path('checkout/',views.checkout,name='checkout'),
  path('shipping/',views.Shipping,name='shipping'),
  path('',RedirectView.as_view(url='dashboard')),
]
