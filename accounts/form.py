from django import forms
from accounts.models import MyProfile
from django.core import validators
from accounts.account_validation import validator

class RegisterForm(forms.ModelForm):
    username = forms.CharField(validators=[validator.username],widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter confirm password','class':'form-control'}))
    class Meta:
        model = MyProfile
        fields = ['username','password','confirm_password','name','gender','phone','profile_pic','register_type']

        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Enter name',"class":'form-control'}),
            'gender': forms.Select(attrs={'id':'gender',"class":'form-control'}),
            'phone' : forms.TextInput(attrs={'placeholder':'Enter Phone',"class":'form-control'}),
            'register_type' : forms.Select(attrs={'id':'type',"class":'form-control'}),
            'profile_pic' : forms.FileInput(attrs={'class':'form-control-file'})
        }

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        print('rakesh',password,confirm_password)
        if password==confirm_password:
            if not len(password)>=6:
                raise validators.ValidationError('Password length is less then 6')
            return self.cleaned_data
        else:
            raise validators.ValidationError('Password and confirm_password does not match')

class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control'}))

class customerForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = "__all__"
        exclude = ['user']



