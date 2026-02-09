from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from restaurant_app.models import ContactMessage, Reservation, Profile


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
        ("12:00:00", "12:00"),
        ("12:15:00", "12:15"),
        ("12:30:00", "12:30"),
        ("12:45:00", "12:45"),
        ("13:00:00", "13:00"),
        ("13:15:00", "13:15"),
        ("13:30:00", "13:30"),
        ("13:45:00", "13:45"),
        ("14:00:00", "14:00"),
        ("14:15:00", "14:15"),
        ("14:30:00", "14:30"),
        ("14:45:00", "14:45"),
        ("15:00:00", "15:00"),
        ("15:15:00", "15:15"),
        ("15:30:00", "15:30"),
        ("15:45:00", "15:45"),
        ("16:00:00", "16:00"),
        ("16:15:00", "16:15"),
        ("16:30:00", "16:30"),
        ("16:45:00", "16:45"),
        ("17:00:00", "17:00"),
        ("17:15:00", "17:15"),
        ("17:30:00", "17:30"),
        ("17:45:00", "17:45"),
        ("18:00:00", "18:00"),
        ("18:15:00", "18:15"),
        ("18:30:00", "18:30"),
        ("18:45:00", "18:45"),
        ("19:00:00", "19:00"),
        ("19:15:00", "19:15"),
        ("19:30:00", "19:30"),
        ("19:45:00", "19:45"),
        ("20:00:00", "20:00"),
        ("20:15:00", "20:15"),
        ("20:30:00", "20:30"),
        ("20:45:00", "20:45"),
        ("21:00:00", "21:00"),
    ]
    
    time_slot = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
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


class RegisterProfileForm(UserCreationForm):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    home_address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    district = forms.CharField(required=True)


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "name", "phone", "home_address", "city", "district"]
        
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit:
            Profile.objects.create(
                user = user,
                name = self.cleaned_data.get("name", ""),
                phone = self.cleaned_data.get("phone", ""),
                home_address = self.cleaned_data.get("home_address", ""),
                city = self.cleaned_data.get("city", ""),
                country = self.cleaned_data.get("country", ""),
            )
            
        return user
