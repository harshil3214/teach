from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Product, Order # Ensure Order is imported
from .forms import ProductForm

# 1. The Home Page
def frontpage(request):
    query = request.GET.get('query', '')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'core/frontpage.html', {
        'products': products,
        'query': query
    })

# 2. Product Detail Page
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})

# 3. Checkout View (Processes the Purchase)
@login_required
def checkout(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Collect data from the checkout form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        # Create the Order in the Admin Panel database
        Order.objects.create(
            product=product,
            buyer=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            zipcode=zipcode,
            paid_amount=product.price
        )
        
        return redirect('success') # Redirect to the success page

    return render(request, 'core/checkout.html', {'product': product})

# 4. Success Page
def success(request):
    return render(request, 'core/success.html')

# 5. User Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontpage')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# 6. User Logout
def logout_view(request):
    logout(request)
    return redirect('frontpage')

# 7. Add Product (Restricted to Admin/Staff)
@login_required
def add_product(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Access Denied: Only administrators can list products.")
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            return redirect('frontpage')
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})