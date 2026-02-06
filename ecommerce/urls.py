from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views as user_views
from adminpanel import views as admin_views

urlpatterns = [

    path('django-admin/', admin.site.urls),

    # ---------------- USER SIDE ----------------
    path('', user_views.home, name='home'),
    path('stock/', user_views.stock, name='stock'),
    path('aboutus/', user_views.aboutus, name='aboutus'),
    path('contact/', user_views.contact, name='contact'),

    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', user_views.logout, name='logout'),

    # ---------------- CART ----------------
    path('add-to-cart/<int:product_id>/', user_views.add_to_cart, name='add_to_cart'),
    path('cart/', user_views.cart_view, name='cart'),
    path('checkout/', user_views.checkout, name='checkout'),
    path('remove-from-cart/<int:item_id>/', user_views.remove_from_cart, name='remove_from_cart'),

    # ---------------- USER ORDERS ----------------
    path('my-orders/', user_views.user_orders, name='user_orders'),

    # ---------------- ADMIN PANEL ----------------
    path('admin-panel/login/', admin_views.admin_login, name='admin_login'),
    path('admin-panel/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),

    path('admin-panel/products/', admin_views.admin_product_list, name='admin_product_list'),
    path('admin-panel/add-product/', admin_views.admin_add_product, name='admin_add_product'),
    path('admin-panel/products/edit/<int:product_id>/', admin_views.admin_edit_product, name='admin_edit_product'),
    path('admin-panel/products/delete/<int:product_id>/', admin_views.admin_delete_product, name='admin_delete_product'),

    path('admin-panel/users/delete/<int:user_id>/', admin_views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/orders/', admin_views.admin_order_dashboard, name='admin_orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
