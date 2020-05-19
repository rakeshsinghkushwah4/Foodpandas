from django import forms
from customer.models import ShippingAddress

class ShippingForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    class Meta:
        """Meta definition for MODELNAMEform."""
        model = ShippingAddress
        fields = ['address','city','state','zipcode']

        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address....'}),
            'city': forms.TextInput(attrs={'class':'form-control','placeholder':'city....'}),
            'state': forms.TextInput(attrs={'class':'form-control','placeholder':'state....'}),
            'zipcode': forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode....'}),

        }