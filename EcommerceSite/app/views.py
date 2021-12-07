from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        total_items = 0
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwear': topwear, 'bottomwear': bottomwear, 
        'mobiles': mobiles, 'total_items': total_items, 'laptops': laptops})

class ProductDetailView(View):
    def get(self, request, id):
        total_items = 0
        product = Product.objects.get(id=id)
        is_incart = False
        if request.user.is_authenticated:
            is_incart = Cart.objects.filter(Q(user=request.user) & Q(product=product.id)).exists()
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'is_incart': is_incart, 'total_items': total_items})

@login_required
def show_cart(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
        carts = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for cart in cart_product:
                temp_amt = (cart.quantity * cart.product.discounted_price)
                amount += temp_amt
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': carts, 'amount': amount, 'total_amount': total_amount, 'total_items': total_items})
        else:
            return render(request, 'app/empty_cart.html', {'total_items': total_items})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    prod_obj = Product.objects.get(id=product_id)
    cart_item = Cart(user=user, product=prod_obj)
    cart_item.save()
    return redirect('/cart')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for cart in cart_product:
                temp_amt = (cart.quantity * cart.product.discounted_price)
                amount += temp_amt
                total_amount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount
            }
            return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for cart in cart_product:
                temp_amt = (cart.quantity * cart.product.discounted_price)
                amount += temp_amt
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': amount + shipping_amount
            }
            return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        # total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for cart in cart_product:
                temp_amt = (cart.quantity * cart.product.discounted_price)
                amount += temp_amt

            data = {
                'amount': amount,
                'total_amount': amount + shipping_amount
            }
            return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    total_items = 0
    users = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'users': users, 'active': 'btn-primary', 'total_items': total_items})

@login_required
def orders(request):
    total_items = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'orders': op, 'total_items': total_items})

@login_required
def change_password(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/changepassword.html', {'total_items': total_items})

def mobile(request, data=None):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'OnePlus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'total_items': total_items})

def laptop(request, data=None):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)
    return render(request, 'app/laptop.html', {'laptops': laptops, 'total_items': total_items})

def topwear(request, data=None):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'below':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html', {'topwear': topwear, 'total_items': total_items})

def bottomwear(request, data=None):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear, 'total_items': total_items})


# def login(request):
#  return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Complete')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for cart in cart_product:
            temp_amt = (cart.quantity * cart.product.discounted_price)
            amount += temp_amt
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount,
     'cart_items': cart_items, 'total_items': total_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        OrderPlaced(user=user, customer=customer, product=cart.product, quantity=cart.quantity).save() 
        cart.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'total_items': total_items})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updated successfully!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'total_items': total_items})