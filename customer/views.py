from django.shortcuts import render,redirect
from seller.models import Product,Tag
from customer.models import Orders, OrderItem
from accounts.models import MyProfile
from django.http import JsonResponse
import json
from customer.form import ShippingForm
import datetime
from django.contrib.auth.decorators import login_required
from accounts.decoratoer import allowed_user


# Create your views here.

@login_required(login_url='login')
@allowed_user(['customer','admin'])
def home(req):
    if req.user.is_authenticated:      
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        orderItem = OrderItem.objects.filter(status='Panding')
        d_order = OrderItem.objects.filter(status='Delivered')
        no_order = len(orderItem)
        delivered = OrderItem.objects.filter(status='Delivered').count()
        panding = orderItem.filter(status='Panding').count()
        cartItem = order.get_cart_items
            
    else:
        items = []
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
        cartItem = order['get_cart_items']
    context = {'orderitem':orderItem,'order':order ,'totalorder':no_order,'delivered':delivered,'panding':panding,'cartItem':cartItem,'d_order':d_order}    
    return render(req,'customer/user_dashboard.html',context)


def store(req):
    tag = Tag.objects.all()
    product = {}
    for i in tag:
        print('tag_type',type(i.name))
        product[i] = Product.objects.filter(tag=i,product_status = True) 
    order = None
    cartItem = None
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        cartItem = order.get_cart_items
    context = {'product':product,'order':order,'cartItem':cartItem,'tag':tag}
    return render(req,'customer/store.html',context)

def cart(req):
    if req.user.is_authenticated:
        customer = req.user.myprofile
        print(customer)
        # try:
        #     obj = Order.objects.get(customer = customer)
        # except Person.DoesNotExist:
        #     obj = Person(customer= customer)
        #     obj.save()
        # Behaind the get_or_create above code is writen 
        # get_or_create method it return tuple (order,create)
        order,create = Orders.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
        cartItem = order['get_cart_items']
    context = {'items':items,'order':order,'cartItem':cartItem}
    return render(req,'customer/cart.html',context)

def checkout(req):
    form = ShippingForm()
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,create = Orders.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []        
        # here when user is not login then bydefault go 0(zero)
        order={'get_cart_total':0,'get_cart_items':0 }
    context = {'items':items,'order':order,'form':form,'cartItem':cartItem}
    return render(req,'customer/checkout.html',context)


def updateItem(req):
    # if data is not come from form
    # data = json.loads(req.data)
    productId = req.POST['productId']
    action = req.POST['action']
    print(productId,action)
    
    customer = req.user.myprofile
    product = Product.objects.get(id=productId)

    order,created = Orders.objects.get_or_create(customer=customer, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product = product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    if orderItem.quantity<1:
        orderItem.quantity=1    
    orderItem.save()
    items={'total_itmes':order.get_cart_items}
    return JsonResponse(items, safe = False)

def cancelOrderItems(req):
    id = req.GET.get('id')
    print('id',id)
    item = OrderItem.objects.get(id = id)
    item.delete()
    return JsonResponse('Product Is delete', safe=False)

def Shipping(req):
    if req.method=="POST":
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        form = ShippingForm(req.POST)
        if form.is_valid():
            ship = form.save(commit=False)
            ship.customer = req.user.myprofile
            ship.order = order
            ship.save()
            order.transiction_id = datetime.datetime.now().timestamp()
            order.complete = True
            order.save()
            return redirect('user_dashboard')
    return render(req,'store/checkout.html')

def prodcut_detail(req,slug):
    product_detail = Product.objects.get(slug = slug)
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order = Orders.objects.get(customer=customer,complete=False)
        cartItem = order.get_cart_items
    else:
        cartItem={'get_cart_total':0,'get_cart_items':0 }
    context = {'product_detail':product_detail,"cartItem":cartItem}
    return render(req,'customer/product_detail.html',context)
# Create your views here.

def more_product(req,tag):
    print('tagss',type(tag))
    product = Product.objects.filter(tag =tag,product_status = True) 
    tag = Tag.objects.get(id=tag)
    if req.user.is_authenticated:
        customer = req.user.myprofile
        order,created = Orders.objects.get_or_create(customer=customer,complete=False)
        cartItem = order.get_cart_items
    context = {'product':product,'tag':tag,'cartItem':cartItem}
    return render(req,'customer/more_product.html',context)
