from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from site_app.forms import SignupForm, EditUserProfileForm, EditAdminProfileForm, UserLoginForm, UserPasswordChangeForm, CheckoutForm, UserSetPasswordForm, EmailForForgotPassword
from django.contrib import messages
#from django.contrib.auth.forms import PasswordChangeForm, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from site_app.models import Cart, Product, Customer, OrderPlaced
from django.db.models import Q
from datetime import *


def base_page(request):
    return render(request, 'site_app/base_page.html')

def index_page(request):
    product_s_t = Product.objects.filter(brand='Sony', category='T')
    product_l_t = Product.objects.filter(brand='Lg', category='T')
    product_p_t = Product.objects.filter(brand='Panasonic', category='T')
    product_a_m = Product.objects.filter(brand='Apple', category='M')
    product_s_m = Product.objects.filter(brand='Samsung', category='M')
    product_o_m = Product.objects.filter(brand='Oppo', category='M')
    product_a_l = Product.objects.filter(brand='Apple', category='L')
    product_as_l = Product.objects.filter(brand='Asus', category='L')
    product_h_l = Product.objects.filter(brand='Hp', category='L')
    #This is user for display number of cart how much items add to cart
    if request.user.is_authenticated:
        list = [c for c in Cart.objects.all() if c.user == request.user]
        count_item = len(list)
        print('Cart item login:=:=:', count_item)
        return render(request, 'site_app/index_page.html', {'product_a_l':product_a_l, 'product_as_l':product_as_l, 'product_h_l':product_h_l,'product_a_m':product_a_m, 'product_o_m':product_o_m, 'product_s_m':product_s_m, 'product_s_t':product_s_t, 'product_l_t':product_l_t, 'product_p_t':product_p_t, 'count_item':count_item, 'firstname':request.user.first_name, 'lastname':request.user.last_name})
    else:
        return render(request, 'site_app/index_page.html', {'product_a_l':product_a_l, 'product_as_l':product_as_l, 'product_h_l':product_h_l,'product_a_m':product_a_m, 'product_o_m':product_o_m, 'product_s_m':product_s_m, 'product_s_t':product_s_t, 'product_l_t':product_l_t, 'product_p_t':product_p_t})


def login_page(request):
    if not request.user.is_authenticated: #If the any user login already don't show login page, Insttead of it redirect on profile page
        if request.method == 'POST':
            fm = UserLoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('http://localhost:8000/site_app/index_page/')
        else:
            fm = UserLoginForm()
        return render(request, 'site_app/login_page.html', {'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/site_app/index_page/')

def signup_page(request):
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account is created')
            fm.save()
            return HttpResponseRedirect('http://localhost:8000/site_app/login_page/')
    else:
        fm = SignupForm()
    return render(request, 'site_app/signup_page.html', {'form':fm})

@login_required(login_url='http://localhost:8000/site_app/login_page')
def myprofile_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'Your profile has been updated !')
                fm.save()
        else:
            fm = EditUserProfileForm(instance=request.user)
        return render(request, 'site_app/myprofile_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def adminprofile_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser==True:
            if request.method == 'POST':
                fm = EditAdminProfileForm(request.POST, instance=request.user)
                if fm.is_valid():
                    messages.success(request, 'Your profile has been updated !')
                    fm.save()
            else:
                fm = EditAdminProfileForm(instance=request.user)
            return render(request, 'admin_app/dashboard.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

# This is showing User and Admin detail in form which can be editable
# def myprofile_page(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             if request.user.is_superuser == True:
#                 fm = EditAdminProfileForm(instance=request.user, data=request.POST)
#                 users = User.objects.all()
#             else:
#                 fm = EditUserProfileForm(instance=request.user, data=request.POST)
#                 users = User.objects.all()
#                 Users = None
#
#             if fm.is_valid():
#                 messages.success(request, 'Your profile has been updated !')
#                 fm.save()
#         else:
#             if request.user.is_superuser == True:
#                 fm = EditAdminProfileForm(instance=request.user)
#                 users = User.objects.all()
#             else:
#                 fm = EditUserProfileForm(instance=request.user)
#                 users = None
#         return render(request, 'site_app/myprofile_page.html', {'form':fm, 'Users':users, 'firstname':request.user.first_name, 'lastname':request.user.last_name})
#     else:
#         return HttpResponseRedirect('http://localhost:8000/site_app/login_page')


@login_required(login_url='http://localhost:8000/site_app/login_page')
def userdetail_page(request):
    if request.user.is_authenticated:
        pi = User.objects.get(id=request.GET['userid'])
        fm = EditAdminProfileForm(instance=pi)
        return render(request, 'site_app/userdetail_page.html', {'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

#User change password with old PasswordChangeForm
@login_required(login_url='http://localhost:8000/site_app/login_page')
def changepassword_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserPasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                messages.info(request, 'Your password has been succeessfully changed, (You may be login again)')
                #messages.success(request, 'Password has been changed successfully !')
                fm.save()
                #messages.info(request, 'Your password has been successfully changed, Please Login')
                return HttpResponseRedirect('http://localhost:8000/site_app/login_page')
        else:
            fm = UserPasswordChangeForm(user=request.user)
        return render(request, 'site_app/changepassword_page.html', {'form': fm, 'firstname':request.user.first_name, 'lastname':request.user.last_name})
    else:
        print('Message:::Anybody is keep accessing your profile in shoppingsite')
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')


# Th showing data filter by brand = Apple mobile
def apple_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    print('Userobject::', userobj)

    if data == None:
        apple_phone = Product.objects.filter(brand='Apple', category='M')
    elif data == 'high':
        apple_phone = Product.objects.filter(brand='Apple', category='M').order_by('-discount_price')
    elif data == 'low':
        apple_phone = Product.objects.filter(brand='Apple', category='M').order_by('discount_price')

    if request.user.is_authenticated:
        return render(request, 'site_app/apple_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'apple_phone':apple_phone, 'userobj':userobj})
    else:
        return render(request, 'site_app/apple_page.html', {'apple_phone':apple_phone})


# It showing data filter by brand = samsung mobile
def samsung_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        samsung_phone = Product.objects.filter(brand='Samsung', category='M')
    elif data == 'high':
        samsung_phone = Product.objects.filter(brand='Samsung', category='M').order_by('-discount_price')
    elif data == 'low':
        samsung_phone = Product.objects.filter(brand='Samsung', category='M').order_by('discount_price')
    print('Samsung_phone::::', samsung_phone)
    if request.user.is_authenticated:
        return render(request, 'site_app/samsung_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'samsung_phone':samsung_phone, 'userobj':userobj})
    else:
        return render(request, 'site_app/samsung_page.html', {'samsung_phone':samsung_phone})

# It showing data filter by brand = oppo mobile
def oppo_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        oppo_phone = Product.objects.filter(brand='Oppo', category='M')
    elif data == 'high':
        oppo_phone = Product.objects.filter(brand='Oppo', category='M').order_by('-discount_price')
    elif data == 'low':
        oppo0_phone = Product.objects.filter(brand='Oppo', category='M').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/oppo_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'oppo_phone':oppo_phone, 'userobj':userobj})
    else:
        return render(request, 'site_app/oppo_page.html', {'oppo_phone':oppo_phone})

# It showing data filter by brand = apple laptop
def lapple_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        apple_laptop = Product.objects.filter(brand='Apple', category='L')
    elif data == 'high':
        apple_laptop = Product.objects.filter(brand='Apple', category='L').order_by('-discount_price')
    elif data == 'low':
        apple_laptop = Product.objects.filter(brand='Apple', category='L').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/lapple_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'apple_laptop':apple_laptop, 'userobj':userobj})
    else:
        return render(request, 'site_app/lapple_page.html', {'apple_laptop':apple_laptop})

def product_detail(request):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    prodid = request.GET.get('pid')
    product = Product.objects.filter(id=prodid)
    cart_exist = False
    if request.user.is_authenticated:
        cart_exist = Cart.objects.filter(Q(product=prodid) & Q(user=user)).exists()
        return render(request, 'site_app/product_detail.html', {'cart_exist':cart_exist, 'product':product, 'firstname':request.user.first_name, 'lastname':request.user.last_name, 'userobj':userobj})
    else:
        # cart_exist = Cart.objects.filter(Q(product=prodid) & Q(user=user)).exists()
        return render(request, 'site_app/product_detail.html', {'product':product})

def lasus_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        asus_laptop = Product.objects.filter(brand='Asus', category='L')
    elif data == 'high':
        asus_laptop = Product.objects.filter(brand='Asus', category='L').order_by('-discount_price')
    elif data == 'low':
        asus_laptop = Product.objects.filter(brand='Asus', category='L').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/lasus_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'asus_laptop':asus_laptop, 'userobj':userobj})
    else:
        return render(request, 'site_app/lasus_page.html', {'asus_laptop':asus_laptop})

def lhp_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        hp_laptop = Product.objects.filter(brand='Hp', category='L')
    elif data == 'high':
        hp_laptop = Product.objects.filter(brand='Hp', category='L').order_by('-discount_price')
    elif data == 'low':
        hp_laptop = Product.objects.filter(brand='Hp', category='L').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/lhp_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'hp_laptop':hp_laptop, 'userobj':userobj})
    else:
        return render(request, 'site_app/lhp_page.html', {'hp_laptop':hp_laptop})

def lg_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        lg_tv = Product.objects.filter(brand='Lg', category='T')
    elif data == 'high':
        lg_tv = Product.objects.filter(brand='Lg', category='T').order_by('-discount_price')
    elif data == 'low':
        lg_tv = Product.objects.filter(brand='Lg', category='T').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/lg_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'lg_tv':lg_tv, 'userobj':userobj})
    else:
        return render(request, 'site_app/lg_page.html', {'lg_tv':lg_tv})

def panasonic_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        panasonic_tv = Product.objects.filter(brand='Panasonic', category='T')
    elif data == 'high':
        panasonic_tv = Product.objects.filter(brand='Panasonic', category='T').order_by('-discount_price')
    elif data == 'low':
        panasonic_tv = Product.objects.filter(brand='Panasonic', category='T').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/panasonic_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'panasonic_tv':panasonic_tv, 'userobj':userobj})
    else:
        return render(request, 'site_app/panasonic_page.html', {'panasonic_tv':panasonic_tv})

def sony_page(request, data=None):
    user = request.user
    userobj = User.objects.filter(id=user.id)
    if data == None:
        sony_tv = Product.objects.filter(brand='Sony', category='T')
    elif data == 'high':
        sony_tv = Product.objects.filter(brand='Sony', category='T').order_by('-discount_price')
    elif data == 'low':
        sony_tv = Product.objects.filter(brand='Sony', category='T').order_by('discount_price')
    if request.user.is_authenticated:
        return render(request, 'site_app/sony_page.html', {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'sony_tv':sony_tv, 'userobj':userobj})
    else:
        return render(request, 'site_app/sony_page.html', {'sony_tv':sony_tv})

@login_required(login_url='http://localhost:8000/site_app/login_page')
def addtocart_page(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('productid')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product, price=product.discount_price).save()
        return HttpResponseRedirect('http://localhost:8000/site_app/show_mycart')
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def show_mycart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # useobj-> for take user id to send with checkout button in template(cart_page.html)
        userobj = User.objects.filter(id=user.id)

        amount = 0.0
        quantity_amount = 0.0
        ship_charg = 50.0
        sub_total = 0.0
        total = 0.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                quantity_amount = (p.quantity * p.product.discount_price)
                amount = amount+quantity_amount
                sub_total = amount
                total = sub_total+ship_charg
        return render(request, 'site_app/cart_page.html', {'firstname':user.first_name, 'lastname':user.last_name, 'cart':cart, 'userobj':userobj, 'sub_total':sub_total, 'ship_charg':ship_charg, 'total':total})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

# Function for increase product Item
def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        print('Product ID::::',  product_id)
        c = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        c.quantity+=1
        c.save()

        amount = 0.0
        quantity_amount = 0.0
        ship_charg = 50.0
        total_amount = 0.0
        sub_total = 0.0

        amount = c.product.discount_price
        quantity = c.quantity

        if quantity >= 1:
            quantity_amount = amount * quantity
            total_amount = quantity_amount
            c.price = total_amount
            c.save()

            sum = 0
            count_price = [p for p in Cart.objects.all() if p.user == request.user]
            for x in count_price:
                sum = x.price + sum
                # print('SUm:::', sum)
                # print('one by one price::', x.price)
                # print('one by one sum:::', sum)
            total = sum+ship_charg

            print('Total wiht shipcharg:::', total)
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'ship_charg':ship_charg,
                'quantity_amount':quantity_amount,
                'total_amount': c.price,
                'sum':sum,
                'total':total
            }
            return JsonResponse(data)

# Function for decrease product Item
def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        print('Product ID:::', product_id)
        obj = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        obj.quantity-=1
        obj.save()

        amount = 0.0
        quantity_amount = 0.0
        ship_charg = 50.0
        total_amount = 0.0
        total = 0.0

        quantity = obj.quantity
        amount = obj.product.discount_price

        if quantity >= 1:
            quantity_amount = amount * quantity
            total_amount = quantity_amount
            obj.price = total_amount
            obj.save()

            sum = 0
            count_price = [p for p in Cart.objects.all() if p.user == request.user]
            for x in count_price:
                sum = x.price + sum

            total = sum + ship_charg
            data = {
                'quantity':obj.quantity,
                'amount':amount,
                'ship_charg':ship_charg,
                'quantity_amount':quantity_amount,
                'total_amount': obj.price,
                'shipcharg':ship_charg,
                'sum':sum,
                'total':total
            }
            return JsonResponse(data)



def delete(request):
    if request.method == 'GET':
        product_id = request.GET['pid']
        print('Product id::', product_id)
        c = Cart.objects.get(Q(product=product_id) & Q(user = request.user))
        print('Cart object=======', c)
        c.delete()
        sum = 0
        shipcharg = 0
        total = 0
        data = {
            'message':'Successfully remove product',
            'sum':sum,
            'shipcharg':shipcharg,
            'total':total
        }
        return JsonResponse(data)
        #return HttpResponseRedirect('http://localhost:8000/site_app/show_mycart')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def address_page(request):
    if request.user.is_authenticated:
        user = request.user
        userid = request.GET.get('userid')
        # userobj = User.object.filter(id=userid)
        userobj = User.objects.filter(id = user.id)
        customerobj = Customer.objects.filter(user=userid)

        if customerobj:
            print('1. Display Edit Form')
            customerdata = Customer.objects.get(user=user)
            print('Customerid:::', customerdata.id)
            fields = {'phone':customerdata.phone, 'address':customerdata.address, 'zipcode':customerdata.zipcode, 'city':customerdata.city, 'state':customerdata.state}
            form_value = CheckoutForm(initial=fields)
            return render(request, 'site_app/editaddress.html', {'firstname':user.first_name, 'lastname':user.last_name, 'form_value':form_value, 'customerdata':customerdata, 'user':user})
        else:
            print('2. Display Address form' )
            if request.method == 'POST':
                fm = CheckoutForm(request.POST)
                if fm.is_valid():
                    p = fm.cleaned_data['phone']
                    print('Phone number:', p)
                    Customer(user=user, phone = fm.cleaned_data['phone'],
                    address = fm.cleaned_data['address'],
                    zipcode = fm.cleaned_data['zipcode'],
                    city = fm.cleaned_data['city'],
                    state = fm.cleaned_data['state']).save()

                    messages.success(request, 'Successfully save your address')
                    user = request.user
                    signupuser = User.objects.filter(id=user.id)
                    customerid = Customer.objects.filter(user = user)
                    amount = 0.0
                    quantity_amount = 0.0
                    ship_charg = 50.0
                    sub_total = 0.0
                    total = 0.0
                    cartdetails = [p for p in Cart.objects.all() if p.user == request.user]
                    if cartdetails:
                        for x in cartdetails:
                            sub_total+=x.price
                    total  = sub_total + ship_charg
                    return render(request, 'site_app/checkout_page.html', {'firstname':user.first_name, 'lastname':user.last_name, 'userobj':userobj, 'cartdetails':cartdetails, 'subtotal':sub_total, 'ship_charg':ship_charg, 'total':total, 'signupuser':signupuser, 'customerid':customerid})
                    #return redirect('/site_app/checkout_page')

            else:
                fm = CheckoutForm()
            return render(request, 'site_app/addressform.html', {'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def update(request):
    if request.user.is_authenticated:
        if request.method=='POST':

            editdata = CheckoutForm(request.POST)
            updatecustomer = Customer(user=request.user)

            updatecustomer.id = request.POST['customerdataid']
            updatecustomer.phone = editdata.data['phone']
            updatecustomer.address = editdata.data['address']
            updatecustomer.zipcode = editdata.data['zipcode']
            updatecustomer.city = editdata.data['city']
            updatecustomer.state = editdata.data['state']

            updatecustomer.save()
            messages.success(request, 'Successfully update details !')
            return redirect('/site_app/checkout_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def checkout_page(request):
    if request.user.is_authenticated:
        user = request.user
        signupuser = User.objects.filter(id=user.id)
        customerid = Customer.objects.filter(user = user)
        amount = 0.0
        quantity_amount = 0.0
        ship_charg = 50.0
        sub_total = 0.0
        total = 0.0
        cartdetails = [p for p in Cart.objects.all() if p.user == request.user]
        if cartdetails:
            for x in cartdetails:
                sub_total+=x.price
        total  = sub_total + ship_charg
        return render(request, 'site_app/checkout_page.html', {'firstname':user.first_name, 'lastname':user.last_name, 'cartdetails':cartdetails, 'subtotal':sub_total, 'ship_charg':ship_charg, 'total':total, 'signupuser':signupuser, 'customerid':customerid})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def buy_now(request):
    if request.user.is_authenticated:
        user = request.user
        userid = request.POST['userid']
        productid = request.POST['productid']
        product = Product.objects.get(id=productid)
        Cart(user=user, product=product, price=product.discount_price).save()
        # userobj = User.object.filter(id=userid)
        userobj = User.objects.filter(id = user.id)
        product = Product.objects.filter(id = productid)
        print('product==', product)
        customerobj = Customer.objects.filter(user=userid)
        print('Customer object:::', customerobj)
        if customerobj:
            print('1. Display Edit Form')
            customerdata = Customer.objects.get(user=user)
            print('Customerid:::', customerdata.id)
            fields = {'phone':customerdata.phone, 'address':customerdata.address, 'zipcode':customerdata.zipcode, 'city':customerdata.city, 'state':customerdata.state}
            form_value = CheckoutForm(initial=fields)
            return render(request, 'site_app/editaddress.html', {'form_value':form_value, 'customerdata':customerdata, 'user':user})
        else:
            print('2. Display Address form' )
            if request.method == 'POST':
                fm = CheckoutForm(request.POST)
                if fm.is_valid():
                    Customer(user=user, phone = fm.cleaned_data['phone'],
                    address = fm.cleaned_data['address'],
                    zipcode = fm.cleaned_data['zipcode'],
                    city = fm.cleaned_data['city'],
                    state = fm.cleaned_data['state']).save()
                    return render(request, 'site_app/checkout_page.html', {'userobj':userobj, 'firstname':user.first_name, 'lastname':user.last_name})
            else:
                fm = CheckoutForm()
            return render(request, 'site_app/addressform.html', {'form':fm})
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def order_page(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        signupuser = User.objects.filter(id = user.id)
        #custid = request.GET.get('customerid')
        custid = request.POST['customerid']
        print('Custid in order_page :::', custid)
        customer_order = Customer.objects.get(id=custid)

        for c in cart:
            OrderPlaced(user=user, customer=customer_order, product=c.product, quantity=c.quantity, price=c.price).save()
        cart.delete()

        list = [o for o in OrderPlaced.objects.all() if o.user == request.user]
        print('OrderPlaced:::', list)
        count_order_item = len(list)

        ship_charg = 50.0
        sub_total = 0.0
        total = 0.0

        if list:
             for x in list:
                 sub_total+=x.price
        total  = sub_total + ship_charg

        # td = date.today()
        # add = td+timedelta(5)
        # delivery_date = add.strftime("%d, %B, %Y")
        #'cart':cart, , 'delivery_date':delivery_date

        dict = {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'customer_order':customer_order, 'order':list, 'count_order_item':count_order_item, 'sub_total':sub_total, 'ship_charg':ship_charg, 'total':total}
        return render(request, 'site_app/order_page.html', dict)
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')

@login_required(login_url='http://localhost:8000/site_app/login_page')
def show_order(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        signupuser = User.objects.filter(id = user.id)
        customer_show_order = Customer.objects.filter(user=request.user)

        print('Cart:::', cart)
        print('SignupUser:::', signupuser)
        print('Customer id::::', customer_show_order)

        list = [o for o in OrderPlaced.objects.all() if o.user == request.user]
        print('OrderPlaced:::', list)
        count_order_item = len(list)

        ship_charg = 50
        sub_total = 0.0
        total = 0.0

        if list is not None:
             for x in list:
                 sub_total+=x.price
             total = sub_total + ship_charg
        order_exist = False
        order_exist = OrderPlaced.objects.filter(user=user).exists()

        dict = {'firstname':request.user.first_name, 'lastname':request.user.last_name, 'customer_show_order':customer_show_order, 'order':list, 'count_order_item':count_order_item, 'sub_total':sub_total, 'ship_charg':ship_charg, 'total':total, 'order_exist':order_exist}
        return render(request, 'site_app/order_page.html', dict)
    else:
        return HttpResponseRedirect('http://localhost:8000/site_app/login_page')
