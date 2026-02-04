from django.shortcuts import render, redirect, get_object_or_404

from main.models import Product, Order , User

from adminpanel.models import AdminAccount

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        admin = AdminAccount.objects.filter(
            username=username,
            password=password
        ).first()

        if admin:
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')

        return render(request, 'admin/login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'admin/login.html')


    return render(request, 'admin/login.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


# ---------- DASHBOARD ----------
def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    context = {
        'product_count': Product.objects.count(),
        'order_count': Order.objects.count(),
        'user_count': User.objects.count(),
        'users': User.objects.all().order_by('-date_joined')
    }

    return render(request, 'admin/dashboard.html', context)

def admin_delete_user(request, user_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    User.objects.filter(id=user_id).delete()
    return redirect('admin_dashboard')



# ---------- PRODUCT MANAGEMENT ----------

def admin_product_list(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})


def admin_add_product(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            category=request.POST['category'],
            
            image=request.FILES['image']
        )
        return redirect('admin_product_list')

    return render(request, 'admin/add_product.html')


def admin_edit_product(request, product_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category')
       

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('admin_product_list')

    return render(request, 'admin/edit_product.html', {'product': product})


def admin_delete_product(request, product_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    Product.objects.filter(id=product_id).delete()
    return redirect('admin_product_list')


# ---------- ORDERS ----------

def admin_order_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    orders = Order.objects.select_related('user').order_by('-created_at')

    return render(request, 'admin/order_dashboard.html', {
        'orders': orders
    })
