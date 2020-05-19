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
from seller import views
from django.views.generic import RedirectView

urlpatterns = [
        path('dashboard/',views.home,name='seller_dashboard'),
        path('product/',views.product,name='product'),
        path('add_product/',views.addProduct,name='add_product'),
        path('customer_detail/<int:pk>',views.customer,name="customer_detail"),
        path('search/<int:pk>',views.search,name='search'),
        path('edit_product/<slug:slug>',views.productEdit,name='edit_product'),
        path('cancel_order/<int:id>',views.Cancel_order,name='cancel_product'),
        path('product_detail/<slug:slug>',views.product_detail,name='seller_product_detail'),
        path('update_order/<int:pk>',views.updateOrder,name="update_order"),
        path('',RedirectView.as_view(url='products'))

]
