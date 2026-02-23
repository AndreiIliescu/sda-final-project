from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from restaurant_app.models import Category, ContactMessage, Reservation, Product, Profile


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Numele Complet", "class": "form-input"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "class": "form-input"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subiectul", "class": "form-input"}),
            "message": forms.Textarea(attrs={"placeholder": "Mesaj", "class": "mesaj-input", "rows": 5}), }
        labels = {"name": "", "email": "", "subject": "", "message": ""}


class ReservationForm(forms.ModelForm):
    TIME_CHOICES = [("12:00:00", "12:00"), ("12:15:00", "12:15"), ("12:30:00", "12:30"), ("12:45:00", "12:45"),
        ("13:00:00", "13:00"), ("13:15:00", "13:15"), ("13:30:00", "13:30"), ("13:45:00", "13:45"),
        ("14:00:00", "14:00"), ("14:15:00", "14:15"), ("14:30:00", "14:30"), ("14:45:00", "14:45"),
        ("15:00:00", "15:00"), ("15:15:00", "15:15"), ("15:30:00", "15:30"), ("15:45:00", "15:45"),
        ("16:00:00", "16:00"), ("16:15:00", "16:15"), ("16:30:00", "16:30"), ("16:45:00", "16:45"),
        ("17:00:00", "17:00"), ("17:15:00", "17:15"), ("17:30:00", "17:30"), ("17:45:00", "17:45"),
        ("18:00:00", "18:00"), ("18:15:00", "18:15"), ("18:30:00", "18:30"), ("18:45:00", "18:45"),
        ("19:00:00", "19:00"), ("19:15:00", "19:15"), ("19:30:00", "19:30"), ("19:45:00", "19:45"),
        ("20:00:00", "20:00"), ("20:15:00", "20:15"), ("20:30:00", "20:30"), ("20:45:00", "20:45"),
        ("21:00:00", "21:00"), ]
    
    time_slot = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    
    class Meta:
        model = Reservation
        fields = ["full_name", "email", "phone", "date", "time_slot", "guests"]
        widgets = {"date": forms.DateInput(attrs={"type": "date", "min": ""}),
            "full_name": forms.TextInput(attrs={"placeholder": "Nume Complet"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Telefon"}),
            "guests": forms.NumberInput(attrs={"min": "1", "max": "9", "value": "2", "id": "id_guests", "class": "form-control", }),}


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
            Profile.objects.create(user = user, username=user.username, email=user.email, name = self.cleaned_data.get("name", ""),
                phone = self.cleaned_data.get("phone", ""), home_address = self.cleaned_data.get("home_address", ""),
                city = self.cleaned_data.get("city", ""), district = self.cleaned_data.get("district", ""), )
            
        return user


class ProductForm(forms.ModelForm):
    new_category = forms.CharField(required=False, label="Categorie nouă", widget=forms.TextInput(attrs={'placeholder': 'Nume Categori'}))
    category_order = forms.IntegerField(required=False, label="Ordinea categoriei", initial=0, widget=forms.NumberInput(attrs={'placeholder': '0'}))

    class Meta:
        model = Product
        fields = ["category", "new_category", "category_order", "name", "description", "image", "price", "availability"]
        labels = { "category": "Categorie existentă", "name": "Nume preparat", "description": "Descriere", "image": "Imagine", 
                  "price": "Preț (lei)", "availability": "Disponibil", }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.category:
            self.fields['category_order'].initial = self.instance.category.order

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        new_category = cleaned_data.get("new_category")

        if not category and not new_category:
            raise forms.ValidationError("Selectează o categorie sau creează una nouă.")

        return cleaned_data

    def save(self, commit=True):
        new_category = self.cleaned_data.get("new_category")
        category_order = self.cleaned_data.get("category_order", 0)

        if new_category:
            category, created = Category.objects.get_or_create(name=new_category.strip())
            category.order = category_order
            category.save()
            self.instance.category = category
        elif self.instance.category and category_order is not None:
            self.instance.category.order = category_order
            self.instance.category.save()

        return super().save(commit)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Parola veche", widget=forms.PasswordInput(attrs={'placeholder': 'Introdu parola actuală'}), required=True)
    new_password1 = forms.CharField(
        label="Parolă nouă", widget=forms.PasswordInput(attrs={'placeholder': 'Introdu noua parolă'}), required=True)
    new_password2 = forms.CharField(
        label="Confirmă parola nouă", widget=forms.PasswordInput(attrs={'placeholder': 'Confirmă noua parolă'}), required=True)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Parola veche introdusă este incorectă.")
        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Cele două parole noi nu corespund.")
        
        return cleaned_data
    
    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        return self.user
