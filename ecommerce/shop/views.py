from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from shop.forms import ProductForm
from shop.models import Product, Category, Cart


# Create your views here.
def base(request):
    return render(request, 'base.html', )


def home(request):
    products = Product.objects.all()
    print(products)
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products ,'categories': categories})

def userhome(request):
    products = Product.objects.all()
    print(products)
    categories = Category.objects.all()
    return render(request, 'user_home.html', {'products': products, 'categories': categories})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        con_pass = request.POST['con_pass']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        if password != con_pass:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.email = email
        myuser.save()
        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        user = authenticate(username=username, password=password)
        products = Product.objects.all()
        categories = Category.objects.all()
        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name
            print(f"name: {fname}, last: {lname}")
            return render(request, 'user_home.html', {'fname': fname, 'lname': lname, 'products': products ,'categories': categories})
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('signin')


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Successfully added new Product")
            return redirect('home')  # Redirect to clear the form and avoid resubmission
    product_form = ProductForm()  # Initialize the form, either after processing POST or for a GET request
    return render(request, 'add_product.html', {'form': product_form})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Successfully updated")
            return redirect('home')  # Redirect to clear the form and avoid resubmission
    product_form = ProductForm(
        instance=product)  # Initialize the form, either after processing POST or for a GET request
    return render(request, 'edit_product.html', {'form': product_form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Successfully deleted")
        return redirect('home')  # Redirect to clear the form and avoid resubmission
    return render(request, 'delete_product.html', {'product': product})

#cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, "Successfully added to cart")
    return redirect('view_cart')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    categories = Category.objects.all()
    total_price = 0
    for item in cart_items:
        item.total = item.product.price * item.quantity
        total_price += item.total
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories':categories,
    }
    return render(request, 'cart.html', context)
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    messages.success(request, "Successfully remove from cart")
    return redirect('view_cart')
