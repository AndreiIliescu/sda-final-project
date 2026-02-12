import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from restaurant_app.forms import ContactForm, ProductForm, RegisterProfileForm, ReservationForm
from restaurant_app.models import Category, Order, OrderItem, Product, Profile, Reservation


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def about_us_page(request):
    return render(request, "about_us.html")


def menu_page(request):
    categories = Category.objects.prefetch_related(
        Prefetch("products", queryset=Product.objects.filter(availability=True))).order_by("order")
    
    context = {"categories": categories, }
    
    return render(request, "menu.html", context)


def contact_us_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save() 
            
            name = form.cleaned_data["name"]
            email_client = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            
            complet_message = f"""
            Ai primit un mesaj nou de pe site-ul Nova Sushi.
            
            Detalii expeditor:
            Nume: {name}
            Email: {email_client}
            
            ----------------------------------------------
            Subiect mail: {subject}
            
            Mesaj:
            {message}
            """
            
            try:
                send_mail(subject=f"Contact Formular: {subject}", message=complet_message, from_email=settings.DEFAULT_FROM_EMAIL, 
                          recipient_list=[settings.EMAIL_HOST_USER], fail_silently=False, )
                
                messages.success(request, "Mesajul a fost trimis și salvat cu succes!")
                return redirect("contact_us")
            
            except Exception as e:
                print(f"Eroare mail: {e}")
                messages.warning(request, "Mesajul a fost salvat, dar a apărut o problemă la notificarea prin email.")
                return redirect("contact_us")
    else:
        form = ContactForm()

    return render(request, "contact_us.html", {"form": form})


def book_reservation_page(request):
    initial_data = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            user_phone = request.user.profile.phone or ""
            user_name = request.user.profile.name or f"{request.user.first_name} {request.user.last_name}".strip()
        else:
            user_phone = ""
            user_name = f"{request.user.first_name} {request.user.last_name}".strip()
        
        initial_data = {"full_name": user_name, "email": request.user.email, "phone": user_phone}

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            
            guests = form.cleaned_data.get("guests")
            if guests < 1:
                messages.error(request, "Numărul de persoane trebuie să fie cel puțin 1.")
            elif guests > 8:
                messages.error(request, "Pentru mai mult de 8 persoane, vă rugăm să ne contactați direct.")
            else:
                if request.user.is_authenticated:
                    reservation.user = request.user
                
                existing_count = Reservation.objects.filter(date=reservation.date, time_slot=reservation.time_slot).count()
                
                if existing_count >= 5:
                    messages.error(request, "Ne pare rău, dar acest interval orar este deja complet ocupat.")
                else:
                    reservation.save()
                    try:
                        send_mail(reservation)
                    except Exception as e:
                        print(f"Eroare la trimitere email: {e}")
                    return render(request, "reservation_success.html", {"reservation": reservation})
    else:
        form = ReservationForm(initial=initial_data)

    return render(request, "reservation.html", {"form": form})


def complaints_and_notifcations_page(request):
    return render(request, "footer_pages/complaints_and_notifications.html")


def payments_and_delivery_page(request):
    return render(request, "footer_pages/payments_and_delivery.html")


def allergen_and_nutritional_values_page(request):
    return render(request, "footer_pages/allergen_list_and_nutritional_values.html")


def terms_and_conditions_page(request):
    return render(request, "footer_pages/terms_and_conditions.html")


def privacy_policy_page(request):
    return render(request, "footer_pages/privacy_policy.html")


def cookies_policy_page(request):
    return render(request, "footer_pages/cookie_policy.html")


def data_security_page(request):
    return render(request, "footer_pages/data_security.html")


def company_identification_data_page(request):
    return render(request, "footer_pages/company_identification_data.html")


def register_user_page(request):
    if request.method == "POST":
        register_form = RegisterProfileForm(request.POST)
        terms_accepted = request.POST.get("terms")
        
        if not terms_accepted:
            messages.error(request, "Trebuie să accepți Termenii și Condițiile pentru a continua.")
        elif register_form.is_valid():
            user = register_form.save()
            
            login(request, user)
            return redirect("home")
    else:
        register_form = RegisterProfileForm()
    
    return render(request, "register.html", {"form": register_form})


class CustomLogInView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    
    
def logout_page(request):
    logout(request)
    return redirect("home")


@login_required
def user_profile_page(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')[:5]
    return render(request, "user_profile.html", {"orders": orders})


class ProfileEditView(UpdateView):
    model = Profile
    template_name = "edit_profile.html"
    fields = ["username", "email", "name", "phone", "home_address", "city", "district"]
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "add_dish.html"
    success_url = reverse_lazy("profile")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "add_dish.html"
    success_url = reverse_lazy("menu")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "delete_dish.html"
    success_url = reverse_lazy("menu")


@login_required
def add_to_favorites(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        profile = request.user.profile

        if product in profile.favorites.all():
            profile.favorites.remove(product)
        else:
            profile.favorites.add(product)

    return redirect("menu")


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get("cart", {})

        if str(product_id) in cart:
            cart[str(product_id)]["quantity"] += 1
        else:
            cart[str(product_id)] = {"name": product.name, "price": float(product.price),
                "image": product.image.url if product.image else "", "quantity": 1, }

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("menu")


def update_cart_quantity(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        action = request.POST.get("action")
        
        if str(product_id) in cart:
            if action == "increase":
                cart[str(product_id)]["quantity"] += 1
                messages.success(request, f"Cantitate actualizată: {cart[str(product_id)]['quantity']}")
            elif action == "decrease":
                if cart[str(product_id)]["quantity"] > 1:
                    cart[str(product_id)]["quantity"] -= 1
                    messages.success(request, f"Cantitate actualizată: {cart[str(product_id)]['quantity']}")
                else:
                    product_name = cart[str(product_id)]["name"]
                    del cart[str(product_id)]
                    messages.success(request, f"{product_name} a fost șters din coș (cantitate 0).")
        
        request.session["cart"] = cart
        request.session.modified = True
    
    return redirect("cart")


def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        
        if str(product_id) in cart:
            product_name = cart[str(product_id)]["name"]
            del cart[str(product_id)]
            messages.success(request, f"{product_name} a fost șters din coș.")
        
        request.session["cart"] = cart
        request.session.modified = True
    
    return redirect("cart")


def cart_page(request):
    cart = request.session.get("cart", {})
    total = 0
    total_items = 0

    for item in cart.values():
        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]
        total_items += item["quantity"]

    context = {"cart": cart, "total": total, "total_items": total_items, }

    return render(request, "cart.html", context)


def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def payment_page(request):
    if request.method == "POST":
        order_data = request.session.get("pending_order")
        
        if not order_data:
            messages.error(request, "Sesiunea ta a expirat. Te rugăm să plasezi din nou comanda.")
            return redirect("cart")
        
        card_number = request.POST.get("card_number")
        card_name = request.POST.get("card_name")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=generate_order_number(),
            full_name=order_data["name"],
            email=order_data["email"],
            phone=order_data["phone"],
            address=order_data["address"],
            city=order_data["city"],
            district=order_data["district"],
            zipcode=order_data["zipcode"],
            payment_method="card",
            total_price=order_data["total"],
        )
        
        for item in order_data["items"]:
            OrderItem.objects.create(
                order=order,
                product_name=item["name"],
                product_price=item["price"],
                quantity=item["quantity"],
            )
        
        del request.session["pending_order"]
        request.session.modified = True
        
        return redirect("order_success", order_id=order.id)
    
    order_data = request.session.get("pending_order")
    
    if not order_data:
        messages.error(request, "Nu există date de comandă. Te rugăm să revii la coș.")
        return redirect("cart")
    
    return render(request, "payment.html", {"order_data": order_data})


def checkout_page(request):
    cart = request.session.get("cart", {})
    
    if not cart:
        messages.error(request, "Coșul tău este gol!")
        return redirect("cart")
    
    initial_data = {}
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        initial_data = {"email": request.user.email, "name": request.user.profile.name or "", "phone": request.user.profile.phone or "",
            "address": request.user.profile.home_address or "", "city": request.user.profile.city or "",
            "district": request.user.profile.district or "", }
    
    if request.method == "POST":
        terms_accepted = request.POST.get("terms")
        
        if not terms_accepted:
            messages.error(request, "Trebuie să accepți Termenii și Condițiile pentru a continua.")
            
            total = 0
            cart_items = []
            for product_id, item in cart.items():
                item["subtotal"] = item["price"] * item["quantity"]
                total += item["subtotal"]
                cart_items.append({"id": product_id, "name": item["name"], "price": item["price"], "quantity": item["quantity"],
                    "subtotal": item["subtotal"], })
            
            return render(request, "checkout.html", {"cart_items": cart_items,  "total": total, "initial_data": initial_data})
        
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        district = request.POST.get("district")
        zipcode = request.POST.get("zipcode")
        payment_method = request.POST.get("payment")
        
        total = 0
        cart_items = []
        for product_id, item in cart.items():
            total += item["price"] * item["quantity"]
            cart_items.append({"name": item["name"], "price": item["price"], "quantity": item["quantity"], })
        
        if payment_method == "card":
            request.session["pending_order"] = {"name": name, "email": email, "phone": phone, "address": address, "city": city,
                "district": district, "zipcode": zipcode, "total": float(total), "items": cart_items, }
            request.session.modified = True
            
            request.session["cart"] = {}
            request.session.modified = True
            
            return redirect("payment")
        
        order = Order.objects.create(user=request.user if request.user.is_authenticated else None, order_number=generate_order_number(),
            full_name=name, email=email, phone=phone, address=address, city=city, district=district, zipcode=zipcode,
            payment_method="cash", total_price=total, )
        
        for product_id, item in cart.items():
            OrderItem.objects.create(order=order, product_name=item["name"], product_price=item["price"], quantity=item["quantity"], )
        
        request.session["cart"] = {}
        request.session.modified = True
        
        return redirect("order_success", order_id=order.id)
    
    total = 0
    cart_items = []
    
    for product_id, item in cart.items():
        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]
        cart_items.append({"id": product_id, "name": item["name"], "price": item["price"], "quantity": item["quantity"],
                           "subtotal": item["subtotal"], })
    
    context = {"cart_items": cart_items, "total": total, "initial_data": initial_data, }
    
    return render(request, "checkout.html", context)


def order_success_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order})


@login_required
def reorder(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = request.session.get("cart", {})
    
    added_items = []
    unavailable_items = []
    
    for order_item in order.items.all():
        try:
            product = Product.objects.get(name=order_item.product_name, availability=True)
            
            if str(product.id) in cart:
                cart[str(product.id)]["quantity"] += order_item.quantity
            else:
                cart[str(product.id)] = {"name": product.name, "price": float(product.price), "image": product.image.url if product.image else "",
                    "quantity": order_item.quantity, }
            
            added_items.append(product.name)
        except Product.DoesNotExist:
            unavailable_items.append(order_item.product_name)
    
    request.session["cart"] = cart
    request.session.modified = True
    
    if added_items:
        messages.success(request, f"Produsele au fost adăugate în coș: {', '.join(added_items)}")
    
    if unavailable_items:
        messages.warning(request, f"Produse indisponibile: {', '.join(unavailable_items)}")
    
    return redirect("cart")
