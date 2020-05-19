from django.contrib import admin
from customer.models import Orders,OrderItem,ShippingAddress
# Register your models here.

admin.site.register(Orders)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Register your models here.
