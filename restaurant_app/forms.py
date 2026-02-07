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
    TIME_CHOICES = [
        ('12:00:00', '12:00'),
        ('12:30:00', '12:30'),
        ('13:00:00', '13:00'),
        ('13:30:00', '13:30'),
        ('14:00:00', '14:00'),
        ('18:00:00', '18:00'),
        ('18:30:00', '18:30'),
        ('19:00:00', '19:00'),
        ('19:30:00', '19:30'),
        ('20:00:00', '20:00'),
        ('20:30:00', '20:30'),
        ('21:00:00', '21:00'),
    ]
    
    time_slot = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
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
