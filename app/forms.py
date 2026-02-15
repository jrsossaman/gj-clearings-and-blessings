from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password




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
        email = self.cleaned_data.get("email", "").strip()
        if not email:
            raise forms.ValidationError("Invalid email.")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A User with that email already exists.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        password = password.strip()
        if not password:
            raise forms.ValidationError("Invalid password.")
        try:
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password", "").strip()
        if not confirm_password:
            raise forms.ValidationError("Please confirm your password.")
        return confirm_password

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
        fields = ['first_name', 'last_name', 'person_or_pet', 'species', 'gender']



class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['client', 'street', 'street_ext', 'city', 'state', 'zip_code', 'country']

    def __init__(self, *args, **kwargs):
        profile=kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if profile:
            self.fields['client'].queryset = Client.objects.filter(profile=profile)
        else:
            self.fields['client'].queryset = Client.objects.none()
    


class ClientSelectForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=Client.objects.filter(is_user=True),
        empty_label="Select a client",
        required=True,
    )



class SessionSheetForm(ModelForm):
    class Meta:
        model = Session_Sheet
        fields = [
            'client', 'date',
            'spiritual1', 'mental1', 'emotional1', 'physical1',
            'chakras', 'cords', 'how_many', 'to_whom', 'hindrances',
            'spiritual2', 'mental2', 'emotional2', 'physical2',
            'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    hindrances = forms.MultipleChoiceField(
        choices=HINDRANCE_TYPE_CHOICES,  # Uses your predefined choices
        widget=forms.CheckboxSelectMultiple,  # Allows multi-selection with checkboxes
        required=False,  # Makes this field optional
    )
    
    def __init__(self, *args, **kwargs):
        clients_queryset = kwargs.pop('clients_queryset', None)
        super().__init__(*args, **kwargs)
        if clients_queryset is not None:
            self.fields['client'].queryset = clients_queryset

    def save(self, commit=True):
        instance = super().save(commit=False)  # Call parent save to handle other fields
        if 'hindrances' in self.cleaned_data:  # Ensure 'hindrances' field has data
            instance.hindrances = ",".join(self.cleaned_data['hindrances'])  # Save multi-choice as a comma-separated string
        if commit:
            instance.save()  # Save the instance to the DB
        return instance



class LocationSheetForm(ModelForm):
    class Meta:
        model = Location_Sheet
        fields = [
            'address', 'date',
            'issues', 'protection',
            'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={"type": "date"}),
        }

    issues = forms.MultipleChoiceField(
        choices=ISSUES_TYPE_CHOICES,  # Uses your predefined choices
        widget=forms.CheckboxSelectMultiple,  # Allows multi-selection with checkboxes
        required=False,  # Makes this field optional
    )

    def __init__(self, *args, **kwargs):
        locations_queryset = kwargs.pop('locations_queryset', None)
        super().__init__(*args, **kwargs)
        if locations_queryset is not None:
            self.fields['address'].queryset = locations_queryset

    def save(self, commit=True):
        instance = super().save(commit=False)  # Call parent save to handle other fields
        if 'issues' in self.cleaned_data:  # Ensure 'hindrances' field has data
            instance.issues = ",".join(self.cleaned_data['issues'])  # Save multi-choice as a comma-separated string
        if commit:
            instance.save()  # Save the instance to the DB
        return instance



class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Enter your password to confirm."
    )