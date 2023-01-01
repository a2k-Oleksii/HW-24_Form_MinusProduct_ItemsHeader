from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MenuItem
from products.models import Product
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    menu_items = MenuItem.objects.all()
    products = Product.objects.filter(Q(display_on_main_page=True) | Q(approved=True)).order_by("-id")
    return render(request, 'main/index.html',
                  {
                      "menu_items": menu_items,
                      "products": products,
                      "count_cart": len(request.session.get('cart', {"products": [], "total": 0})["products"]),
                      "total": 0,
                  })


def sign_up(request):
    if request.method == "POST":
        user = User()
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.set_password(request.POST.get('password'))
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()
        user = authenticate(request, username=user.username, password=user.password)
        if user:
            login(request, user)
        return redirect('/')
    else:
        return render(request, 'main/sign-up.html', {})


def sign_in(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
        return redirect('/')
    else:
        return render(request, 'main/sign-in.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if request.session.get('cart', False):
        is_product_already_added = False
        for el in request.session.get('cart', {'products': [], 'total': 0})['products']:
            if el['id'] == id:
                el['count'] += 1
                request.session['cart']['total'] += product.price
                el['price'] += product.price
                is_product_already_added = True
        if not is_product_already_added:
            request.session['cart']['total'] += product.price
            request.session['cart']['products'].append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'count': 1,
            })
    else:
        request.session['cart'] = {
            'products': [],
            'total': 0,
        }
        request.session['cart']['total'] = product.price
        request.session['cart']['products'].append({
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'count': 1,
        })
    request.session.modified = True
    return redirect('/cart')


def take_away_to_cart(request, id):
    # Take away from cart one unit product
    product = Product.objects.get(id=id)
    if request.session.get('cart', False):
        for el in request.session.get('cart', {'products': [], 'total': 0})['products']:
            if el['id'] == id and el['count'] >= 1:
                el['count'] -= 1
                request.session['cart']['total'] -= product.price
                el['price'] -= product.price
    request.session.modified = True
    return redirect('/cart')


def show_cart(request):
    return render(request, 'main/cart.html', {
        'products': request.session.get('cart', {"products": [], "total": 0})["products"],
        "total": request.session.get('cart', {"products": [], "total": 0})["total"],
        "count_cart": len(request.session.get('cart', {"products": [], "total": 0})["products"]),
    })


def delete_cart(request, id):
    if request.session.get("cart", False):
        products = request.session["cart"]["products"]
        for index in range(len(products)):
            if products[index]["id"] == int(id):
                request.session["cart"]["total"] -= products[index]["price"]
                del request.session["cart"]["products"][index]
                request.session.modified = True
                break
        return redirect("/cart")
