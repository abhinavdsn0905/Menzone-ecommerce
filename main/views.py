from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import UserProfile, Product,Order,OrderItem,CartItem
from decimal import Decimal
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from .models import EmailOTP
import random
from django.contrib.auth import login
# ---------- LANDING PAGE ----------

def home(request):
    return render(request, 'index.html')


def stock(request):
   
    products = Product.objects.all()
    return render(request, 'stock.html', {'products': products})


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        query = request.POST.get('query')

        return render(request, 'contact.html', {
            'success': 'Thank you! We will contact you soon.'
        })

    return render(request, 'contact.html')


# ---------- REGISTER ----------

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        UserProfile.objects.create(
            user=user,
            address=address,
            pincode=pincode
        )

        # EMAIL
        subject = "Welcome to MENZONE"
        message = f"""
                    Hi {name},

                    Welcome to MENZONE! 

                    We're excited to have you on board.
                    Explore the latest men’s fashion, premium collections, and exclusive deals.

                    Happy Shopping 
                    Team MENZONE
                    """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        return redirect('login')

    return render(request, 'register.html')
# ---------- USER LOGIN ----------

def login_user(request):
    context = {}

    # OTP
    if request.method == "POST" and 'send_otp' in request.POST:
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            context['error'] = "Email not registered"
            return render(request, 'login.html', context)

        otp = str(random.randint(100000, 999999))

        # Save OTP 
        EmailOTP.objects.create(email=email, otp=otp)

        send_mail(
            "MENZONE Login OTP",
            f"Your OTP is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        request.session['login_email'] = email
        context['otp_sent'] = True
        context['email'] = email
        return render(request, 'login.html', context)

    # VERIFY OTP
    if request.method == "POST" and 'verify_otp' in request.POST:
        email = request.session.get('login_email')
        entered_otp = request.POST.get('otp')

        otp_record = EmailOTP.objects.filter(
            email=email,
            otp=entered_otp
        ).first()

        if otp_record:
            user = User.objects.get(email=email)
            login(request, user)

            otp_record.delete()
            del request.session['login_email']

            return redirect('home')

        context['error'] = "Invalid OTP"
        context['otp_sent'] = True
        context['email'] = email
        return render(request, 'login.html', context)

    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('home')

# ---------- CART ----------
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')



def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total_items = sum(item.quantity for item in cart_items)
    grand_total = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'grand_total': grand_total
    }

    return render(request, 'cart.html', context)

from django.contrib.auth.decorators import login_required

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    order = Order.objects.create(
        user=request.user,
        status='Placed'
    )

    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        price = Decimal(product.price) * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        total += price

    order.total_amount = total
    order.save()

    subject = f"Order Confirmed - MENZONE (Order #{order.id})"

    message = f"""
Hello {request.user.first_name or request.user.username},

Thank you for shopping with MENZONE 🖤

🧾 Order Details
-------------------------
Order ID: {order.id}
Total Amount: ₹{order.total_amount}
Order Status: {order.status}

We’ll notify you once your order is shipped.

Happy Shopping!
MENZONE Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False
    )

    request.session['cart'] = {}

    return redirect('user_orders')

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_orders.html', {'orders': orders})

def stock(request):
    shirts = Product.objects.filter(category='Shirt')
    tshirts = Product.objects.filter(category='Tshirt')
    jeans = Product.objects.filter(category='Jeans')
    jackets = Product.objects.filter(category='Jacket')

    context = {
        'shirts': shirts,
        'tshirts': tshirts,
        'jeans': jeans,
        'jackets': jackets,
    }
    return render(request, 'stock.html', context)
