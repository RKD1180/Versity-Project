from django import forms
from django.contrib import auth
from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import authenticate, login as dj_login
from django.views.generic import TemplateView
from .forms import CustomerProfileFrom
# from .forms import CustomerRegistrationFrom
from django.db.models import Q
from django.http import JsonResponse


def home(request):
    mobile = Product.objects.filter(category='M')
    laptop = Product.objects.filter(category='L')
    airphone = Product.objects.filter(category='A')
    tablet = Product.objects.filter(category='T')
    products = {'mobile': mobile, 'laptop': laptop,
                'airphone': airphone, 'tablet': tablet}

    return render(request, 'app/home.html', products)


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount})


def update_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': total_amount,
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': total_amount,
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            data = {

                'amount': amount,
                'totalamount': total_amount,
            }
            return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def orders(request):
    return render(request, 'app/orders.html')


# class change_password(TemplateView):
#     def chnpw(args):
#         return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Xaomi' or data == 'Nokia' or data == 'Walton':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'Hp' or data == 'Asus':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptop': laptop})


def airphone(request, data=None):
    if data == None:
        airphone = Product.objects.filter(category='A')
    elif data == 'Xaomi' or data == 'Nokia' or data == 'Realme' or data == 'Remax':
        airphone = Product.objects.filter(category='A').filter(brand=data)
    return render(request, 'app/airphone.html', {'airphone': airphone})


def tablet(request, data=None):
    if data == None:
        tablet = Product.objects.filter(category='T')
    elif data == 'Xaomi' or data == 'Nokia' or data == 'Hp' or data == 'Asus':
        tablet = Product.objects.filter(category='T').filter(brand=data)
    return render(request, 'app/tablet.html', {'tablet': tablet})


def login(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        password = request.POST['loginpassword']

        user = authenticate(request, username=loginusername,
                            password=password)
        if user is not None:
            dj_login(request, user)

            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/login")
    # return HttpResponse("404- Not found")
    return render(request, 'app/login.html')


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')


def CustomerRegistrationView(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        # if len(username) < 10:
        #     messages.error(
        #         request, " Your user name must be under 10 characters")
        #     return redirect('/registration')

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('/registration')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('/registration')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, " Your onlineshop has been successfully created")
        return redirect('/login')

    else:
        return render(request, 'app/customerregistration.html')


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})


class profile(View):
    def get(self, request):
        form = CustomerProfileFrom()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileFrom(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            # phone_number = form.cleaned_data['phone_number']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            division = form.cleaned_data['division']
            reg = Customer(user=user, name=name, locality=locality,
                           city=city, zipcode=zipcode, division=division)
            reg.save()
            messages.success(
                request, 'Congratulations Profile Created successfuly')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


def contactus(request):
    return render(request, 'app/contactus.html')


def aboutus(request):
    return render(request, 'app/aboutus.html')
