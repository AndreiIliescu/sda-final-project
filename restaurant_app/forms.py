from django import forms
from restaurant_app.models import ContactMessage, Reservation


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Numele tău", "class": "form-input"}),
            "email": forms.EmailInput(attrs={"placeholder": "Adresa de email", "class": "form-input"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subiectul mesajului", "class": "form-input"}),
            "message": forms.Textarea(attrs={
                "placeholder": "Scrie mesajul tău aici ...", 
                "class": "mesaj-input",
                "rows": 5
            }),
        }
        labels = {
            "name": "", "email": "", "subject": "", "message": ""
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["full_name", "email", "phone", "date", "time_slot", "guests"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "min": ""}),
            "full_name": forms.TextInput(attrs={"placeholder": "Nume Complet"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Telefon"}),
            "guests": forms.NumberInput(attrs={
                "min": "1", 
                "max": "9",
                "value": "2",
                "id": "id_guests",
                "class": "form-control",
            }),
        }
