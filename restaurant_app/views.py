from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from restaurant_app.forms import ContactForm, RegisterProfileForm, ReservationForm
from restaurant_app.models import Category, Product, Profile, Reservation


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def about_us_page(request):
    return render(request, "about_us.html")


def menu_page(request):
    categories = Category.objects.prefetch_related(
        Prefetch("products", queryset=Product.objects.filter(availability=True))).order_by("order")
    
    context = {
        "categories": categories,
    }
    
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
            
            -----------------------
            Subiect mail: {subject}
            
            Mesaj:
            {message}
            """
            
            try:
                send_mail(
                    subject=f"Contact Formular: {subject}",
                    message=complet_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                
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
        
        initial_data = {
            "full_name": user_name,
            "email": request.user.email,
            "phone": user_phone
        }

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
                
                existing_count = Reservation.objects.filter(
                    date=reservation.date, 
                    time_slot=reservation.time_slot
                ).count()
                
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
    return render(request, "user_profile.html")


class ProfileEditView(UpdateView):
    model = Profile
    template_name = "edit_profile.html"
    fields = ["username", "email", "name", "phone", "home_address", "city", "district"]
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.profile
