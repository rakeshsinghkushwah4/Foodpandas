from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.form import RegisterForm ,UserLogin
from django.contrib.auth.models import User, Group
from accounts.models import MyProfile
from accounts.form import customerForm
from customer.models import Orders
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from accounts.token_generator import account_activation_token
from django.core import validators
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decoratoer import unauthenticated_user

@unauthenticated_user
def register(req):
    form = RegisterForm()
    if req.method == "POST":
        form = RegisterForm(req.POST,req.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=req.POST.get('username'),password=req.POST.get('password'),email=req.POST.get('username'))
            # Here user is save but not active therefore user not login
            user.is_active = False
            print(req.POST.get('name'))
            user.myprofile.name= req.POST.get('name')
            user.myprofile.gender= req.POST.get('gender')
            user.myprofile.phone= req.POST.get('phone')
            user.myprofile.register_type= req.POST.get('register_type')
            group = Group.objects.get(name=req.POST['register_type'])
            user.groups.add(group)
            user.myprofile.profile_pic= req.FILES.get('profile_pic')
            user.save()
            # we get the current site from the request. it return domain name like www.rakesh.com
            current_site = get_current_site(req)
            email_subject = 'Activate Your Account'
            # here we create message in the html form in the we pass user,domain,uid,token
            message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('username')
            # to_email = form.POST.get('username')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
            print('rake',current_site)
    return render(req,'accounts/register.html',{'form':form})

# Here we check the given token is vaild or not if valid so user is activate
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

@unauthenticated_user
def user_login(req):
    form = UserLogin()
    if req.method == 'POST':
        form = UserLogin(req.POST)
        if form.is_valid():
            # Here we check user is available in the database or not if available then is authenticate the user
            # But not set in session so because of this we can't get the info of authenticate user
            user=authenticate(username=req.POST['username'],password=req.POST['password'])
            if user is not None:
                # Here login is set the user in session. Now we get whole info of user
                login(req,user)
                print('login')
                return redirect('seller_dashboard')
            else:
                messages.info(req,'Username or Password is incorrect ')
    return render(req,'accounts/login.html',{'form':form})

@login_required(login_url='login')
def user_logout(req):
    if req.user.is_authenticated:
        logout(req)
        return redirect('login')

# Password reset
@unauthenticated_user
def password_reset(req):
    if req.method=="POST":
        username= req.POST.get('email')
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('Please enter the valid username this username is not found ')
        current_site = get_current_site(req)
        email_subject = 'Reset Password of Your Account'
    # here we create message in the html form in the we pass user,domain,uid,token
        message = render_to_string('accounts/password_reset.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(email_subject, message, to=[username])
        email.send()
        return HttpResponse('We ave sent you an email, please confirm your email address to complete registration')
    else:
        return HttpResponse('enter the username')

def password_activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user = user.username
        print('uid',user)
        return render(request, 'accounts/reset_change_password.html',{'user':user})
    else:
        return HttpResponse('Activation link is invalid!')

@unauthenticated_user
def change_password(req,user):
    user = User.objects.get(username=user)
    password = req.POST.get('password')
    confirm_password = req.POST.get('confirm_password')
    if password==confirm_password:
        if len(password) >= 6 :
            user.set_password(confirm_password)
            user.save()
            return redirect('login')
        else:
            messages.info(req,"Password is less the 6 character")
    else:
        messages.info(req,'Password and confirm password is not matched ')
    return render(req, 'accounts/reset_change_password.html', {'user': user})

@login_required(login_url='login')
def profile(req):
    customer = req.user.myprofile
    order,created = Orders.objects.get_or_create(customer=customer,complete=False)
    cartItem = order.get_cart_items
    try:
        user = req.user.myprofile 
        print('user',user)
        form  = customerForm(instance=user)
        print('rakesh')
        if req.method=='POST':
            form = customerForm(req.POST,req.FILES,instance=user)
            if form.is_valid:
                print('form is valid')
                form.save()
    except:
        pass
    context={'form':form,'cartItem':cartItem}
    return render(req,'accounts/accounts_settings.html',context)




