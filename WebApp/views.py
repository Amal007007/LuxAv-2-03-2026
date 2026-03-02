from platform import uname

from django.shortcuts import render,redirect
from AdminApp.models import *
from WebApp.models import *
from django.contrib import messages


# Create your views here.

def home_page(request):
    Categories = CategoryDb.objects.all()
    AllProducts = ProductDb.objects.order_by('id')[:8]
    NewProducts = ProductDb.objects.order_by('-id')[:4]
    return render(request,"Home.html",{'Categories':Categories,'AllProducts':AllProducts,'NewProducts':NewProducts})

def about_page(request):
    Categories = CategoryDb.objects.all()
    return render(request,"About.html",{'Categories':Categories})
def all_products(request , cat_name=None):
    Categories = CategoryDb.objects.all()
    Products = ProductDb.objects.all()
    product_filtered = ProductDb.objects.filter(Category_Name=cat_name)
    return render(request,"All_Products.html",{'Products':Products,'Categories':Categories,'product_filtered':product_filtered})

def filtered_products(request, cat_name):
    Categories = CategoryDb.objects.all()
    product_filtered = ProductDb.objects.filter(Category_Name=cat_name)
    return  render(request,"Filtered_Product.html",{'product_filtered':product_filtered,'Categories':Categories})

def single_page(request,product_id):
    Categories = CategoryDb.objects.all()
    F_Products = ProductDb.objects.order_by('id')[:6]
    SingleProduct = ProductDb.objects.filter(id=product_id)
    return render(request,"Single_Page.html",{'Categories':Categories,'F_Products':F_Products,'SingleProduct':SingleProduct})

def contact(request):
    Categories = CategoryDb.objects.all()
    return  render(request,"Contact.html",{'Categories':Categories})

def save_contact(request):
    if request.method == "POST":
        name = request.POST.get('c_name')
        email = request.POST.get('c_email')
        subject = request.POST.get('c_subject')
        message = request.POST.get('c_message')
        obj = ContactDb(Name=name,Email=email,Subject=subject,Message=message)
        obj.save()
        return redirect('contact')

def sign_in(request):
    return render(request,"Sign_In.html")

def sign_up(request):
    return render(request,"Sign_Up.html")


def save_sign_up(request):
    if request.method == "POST":
        uname = request.POST.get('sup_name')
        email = request.POST.get('sup_email')
        paswd = request.POST.get('sup_password')
        cnf_paswd = request.POST.get('sup_cnf_password')

        if paswd == cnf_paswd:
            if uname and email and paswd:
                obj = UserDb(Username=uname, Email_ID=email, Password=paswd)
                if UserDb.objects.filter(Username =  uname, Password = paswd).exists():
                    print("Username already exist !")
                    return redirect(sign_up)
                elif UserDb.objects.filter(Email_ID=email).exists():
                    print("Email id already exists")
                    return redirect(sign_up)
                else:
                    obj.save()
                    return redirect('sign_in')
            else:
                return redirect(sign_up)

        return redirect('sign_up')

def services(request):
    Categories = CategoryDb.objects.all()
    service = ServiceDb.objects.all()
    return render(request,"Services.html",{'service':service,'Categories':Categories})

def user_login(request):
    if request.method == "POST":
        uname = request.POST.get('sin_username')
        paswd = request.POST.get('sin_password')
        if UserDb.objects.filter(Username=uname, Password=paswd).exists():
            request.session['Username'] = uname
            request.session['Password'] = paswd
            return redirect(home_page)
        else:
            return redirect(sign_in)
    else:
        return redirect(sign_in)

def log_out(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(home_page)

def payment(request):
    return render(request,"Payment.html")
def cart(request):
    Categories = CategoryDb.objects.all()
    data = CartDb.objects.filter(Cart_Username=request.session['Username'])
    sub_total = 0
    delivery = 0
    grand_total = 0
    for i in data:
        sub_total += i.Cart_TotalPrice
        if sub_total > 1000:
            delivery = 0
        elif sub_total > 500:
            delivery = 50
        else:
            delivery = 100
        grand_total = sub_total + delivery
    return render(request, "Cart.html", {'data': data,
    'sub_total': sub_total,'delivery': delivery, 'grand_total': grand_total,'Categories':Categories})

def add_cart(request):
    if request.method == "POST":
        username = request.POST.get('username')
        product_name = request.POST.get('product_name')
        price = request.POST.get('si_price')
        total_price = request.POST.get('si_total_price')
        quantity = request.POST.get('quantity')
        pro = ProductDb.objects.filter(Product_Name=product_name).first()
        img = pro.Product_Image if pro else None
        obj = CartDb(Cart_Username=username, Cart_ProductName=product_name, Cart_Quantity=quantity, Cart_Price=price, Cart_TotalPrice=total_price,Cart_ProductImage=img)
        obj.save()
        messages.success(request,"Successfully Added to Cart")
        return redirect('cart')
    messages.error(request,"Error Please Contact Support")
    return render(request,"single_page")

def checkout(request):
    data = CartDb.objects.filter(Cart_Username=request.session['Username'])
    Categories = CategoryDb.objects.all()
    sub_total = 0
    delivery = 0
    grand_total = 0
    for i in data:
        sub_total += i.Cart_TotalPrice
        if sub_total > 1000:
            delivery = 0
        elif sub_total > 500:
            delivery = 50
        else:
            delivery = 100
        grand_total = sub_total + delivery
    return render(request, "Checkout.html",
                  {'data': data, 'sub_total': sub_total, 'delivery': delivery, 'grand_total': grand_total,'Categories':Categories}, )

def add_checkout(request):
    if request.method == "POST":
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        address = request.POST.get('address')
        place = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        final_price = request.POST.get('final_price')
        obj = OrderDb(First_Name=f_name, Last_Name=l_name, Place=place, Email_ID=email,
                      Address=address, Mobile= mobile, State=state, Pincode=pincode, TotalPrice=final_price)
        obj.save()
        return redirect(payment)