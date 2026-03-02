from django.urls import path
from WebApp import views

urlpatterns=[
    path('Home/',views.home_page, name="home"),
    path('About/',views.about_page, name="about"),
    path('Products/',views.all_products, name="all_products"),
    path('Products/<cat_name>',views.all_products, name="all_products"),
    path('ProductFiltered/<cat_name>/', views.filtered_products, name="filtered_products"),
    path('ProductDetails/<int:product_id>/', views.single_page ,name="single_page"),
    path('ProductDetails/<cid>/', views.single_page ,name="single_page"),
    path('Contact/', views.contact ,name="contact"),
    path('save_contact/', views.save_contact ,name="save_contact"),
    path('sign_in/', views.sign_in ,name="sign_in"),
    path('sign_up/', views.sign_up ,name="sign_up"),
    path('save_sign_up/', views.save_sign_up ,name="save_sign_up"),
    path('services/', views.services ,name="services"),
    path('user_login/', views.user_login ,name="user_login"),
    path('log_out/', views.log_out ,name="log_out"),
    path('cart/', views.cart ,name="cart"),
    path('add_cart/', views.add_cart ,name="add_cart"),
    path('Checkout/', views.checkout ,name="checkout"),
    path('payment/', views.payment ,name="payment"),
    path('add_checkout/', views.add_checkout ,name="add_checkout"),

]