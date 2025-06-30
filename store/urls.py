from django.urls import path
from .import views
from .import api_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('api/products/', api_views.api_products, name='api_products'),
    path('api/my-order/', api_views.api_my_order, name='api_my_order'),
    path('order-history', views.order_history, name='order_history'),
    path('', views.product_list, name='product_list'),
]
