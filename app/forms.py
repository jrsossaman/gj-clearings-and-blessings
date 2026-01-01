from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email Address"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password"
        })
    )



class UserCreationForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email Address"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password"
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A User with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    


class PrimaryClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name']
    first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name'
    }))



class AdditionalClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name']
    first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'Email (optional)'
    }))



class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_type', 'street', 'street_ext', 'city', 'state', 'zip_code', 'country']
    


class ClientSelectForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.filter(is_user=True),
        empty_label="Select a client",
        required=True,
        widget=forms.Select(attrs={
            'class': 'select2'
        })
    )



class SessionSheetForm(ModelForm):
    class Meta:
        model = Session_Sheet
        fields = [
            'client', 'date',
            'spiritual1', 'mental1', 'emotional1', 'physical1',
            'chakras', 'cords', 'hinderances', 'dark_entities', 'attacks',
            'social', 'viruses',
            'spiritual2', 'mental2', 'emotional2', 'physical2'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        clients_queryset = kwargs.pop('clients_queryset', None)
        super().__init__(*args, **kwargs)
        if clients_queryset is not None:
            self.fields['client'].queryset = clients_queryset