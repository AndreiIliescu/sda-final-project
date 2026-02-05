from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from restaurant_app.forms import ContactForm
from restaurant_app.models import Category, Product


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
