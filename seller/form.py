from django import forms
from django.contrib.auth.models import User
from seller.models import Product
from customer.models import OrderItem

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['slug','seller']

class searchForm(forms.Form):
    Status = (('Status','Status'),('Panding','Panding'),('Delivered','Delivered'))
    product = Product.objects.all()
    pro = (('Product','Prodcut'),)
    for p in product:
        pro= pro+((str(p),str(p)),)
    status = forms.ChoiceField(choices=Status,required=False,initial='None')
    products = forms.ChoiceField(choices = pro,required=False,initial='None')

class orderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']
