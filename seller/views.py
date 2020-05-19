from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.decoratoer import seller_only,allowed_user
from seller.form import AddProductForm,searchForm
from customer.models import ShippingAddress
from accounts.models import MyProfile
from seller.form import Product,orderForm
from customer.models import OrderItem,Orders
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core import serializers
import json 
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

@login_required(login_url='login')
@seller_only(url='user_dashboard')
@allowed_user(['seller','admin'])
def home(req):
    orderitem = OrderItem.objects.filter(product__seller=req.user.myprofile,order__complete=True,status="Panding")
    orderitem = orderitem
    orders_display = orderitem[:5]
    customer = set()
    for cu in orderitem:
        customer.add(cu.order.customer)
    total_order = orderitem.count()
    total_delivered = orderitem.filter(status='Delivered').count()
    total_panding = orderitem.filter(status='Panding').count()
    orders_display = orderitem[:5]
    context = {'orderitem':orders_display,'totalorder':total_order,'delivered':total_delivered,'panding':total_panding,'customer':customer}
    return render(req,'seller/dashboard.html',context)

@login_required(login_url='login')
@seller_only(url='store')
@allowed_user(['seller','admin'])
def product(req):
    product = Product.objects.filter(seller = req.user.myprofile)
    context = {'product':product}
    return render(req,'seller/product.html',context)

@login_required(login_url='login')
@seller_only(url='store')
@allowed_user(['seller','admin'])
def product_detail(req,slug):
    product = Product.objects.get(slug = slug)
    context = {'product':product}
    return render(req,'seller/product_detail.html',context)

@login_required(login_url='login')
@allowed_user(['seller','admin'])
def productEdit(req,slug):
    edit = 'edit'
    product = Product.objects.get(slug= slug)
    form = AddProductForm(instance=product)
    if req.method=="POST":
        form = AddProductForm(req.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    context={'form':form,"edit":edit,'id':slug}
    return render (req,'seller/add_product.html',context)

@login_required(login_url='login')
@allowed_user(['seller','admin'])
def addProduct(req):
    form = AddProductForm()
     # here extra is tall how many form you get 5 or 10 or so many
    # form = orderForm(initial = {"customer":customer})
    # formset = AddProductForm(queryset=Order.objects.none()
    if req.method=="POST":
        # form = orderForm(req.POST)
        form = AddProductForm(req.POST,req.FILES)
        if form.is_valid():
            # Here we are not saving this form but form is take all field 
            pro = form.save(commit=False)
            pro.seller = req.user.myprofile
            pro.save()    
            return redirect('/')
        else:
            print(form.errors)
            # print('form',form)
    context = {'form':form}
    return render(req,'seller/add_product.html',context)


@login_required(login_url='login')
def search(req,pk):
    order1 = None
    customer = MyProfile.objects.get(id=pk)
    order = Orders.objects.filter(customer=customer,complete=True)
    maindata = []
    item_list = []
    for i in order:
        item_list.append(i.orderitem_set.all())
    
    if req.method=='POST' and req.is_ajax():
        form = searchForm(req.POST)
        if form.is_valid():
            # If form is valid then form.cleaned_data is work in the form condition
            status = form.cleaned_data['status']
            product = form.cleaned_data['products'] 
            print(status,product)
            for o in order:
                print('orde',o.orderitem_set.all())
                print('roder',o.orderitem_set.filter(product__name__icontains=product))
                if status or product:
                    if status !='Status' and product !='Product':
                        order1 = o.orderitem_set.filter(Q(status__icontains=status)&
                                    Q(product__name__icontains=product)).values('id','product__name','product__Category','cr_date','status')
                        print(type(order1))
                    elif status == "Status" and product == "Product":
                        order1 = o.orderitem_set.all().values('id','product__name','product__Category','cr_date','status')
                    else:
                        order1 = o.orderitem_set.filter(Q(status__icontains=status) |
                                            Q(product__name__icontains=product)).values('id','product__name','product__Category','cr_date','status')
                    # values is always return queryValues not a query datatype
                    # But when we are not apply value in the query the it return query datatype
                    # in query datatype we use following serializer use

                    #serdata = serializers.serialize("json", order1)

                    #But datatype is queryValue then we use below serializer
                    serdata = json.dumps(list(order1),cls=DjangoJSONEncoder)
                    maindata.append(serdata)
            print('maindata',maindata)
            return JsonResponse(maindata,safe=False)
    context = {'order1':order1,'customer':customer}
    return render(req,'seller/customer.html',context)


@login_required(login_url='login')
@allowed_user(['seller','admin'])
def customer(req,pk):
    search_form = searchForm()
    customer = MyProfile.objects.get(id=pk)
    # Thus order is show which current seller is logged in or seller add the product
    order = Orders.objects.filter(customer=customer,complete=True)
    total_order = 0
    print('ord',order)
    item_list = []
    for i in order:
        total_order += i.orderitem_set.all().count()
        item_list.append(i.orderitem_set.all())    
    print('item',item_list)
    context = {'customer':customer,'search_form':search_form,'order':item_list,'total_order':total_order}
    return render(req,'seller/customer.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','seller'])
def Cancel_order(req,id):
    product = Product.objects.get(id=id)
    product.image.delete()
    product.delete()
    return redirect('product')
 
 
@login_required(login_url='login')
@allowed_user(['seller','admin'])
def updateOrder(req,pk):    
    order = OrderItem.objects.get(pk=pk)
    print('sdfkf',order.order.id)
    id = order.order
    shipping = ShippingAddress.objects.get(order=order.order)
    print('sdflsdfj',shipping)
    form = orderForm(instance=order)
    if req.method=="POST":
        form = orderForm(req.POST, instance=order)
        if form.is_valid():    
            form.save()
            return redirect('/')
    context = {'form':form,'order':order,'shipping':shipping}
    return render(req,'seller/order_form.html',context)

