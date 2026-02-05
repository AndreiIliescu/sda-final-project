from django import forms
from restaurant_app.models import ContactMessage


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
