from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

# dev user creds: email@email.com / test123

def handle_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                form.add_error(None, "Invalid email or password.")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



def admin_dashboard(request):
    form = ClientSelectForm()
    selected_client = None
    if request.method == "POST":
        form = ClientSelectForm(request.POST)
        if form.is_valid():
            selected_client = form.cleaned_data["client"]
    return render(request, "admin_dashboard.html", {"form": form, "selected_client": selected_client})



User = get_user_model()

def admin_user_creation(request):
#    if not request.user.is_staff:
#        return redirect("login")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]

            user = User.objects.create_user(username=email, email=email)
            user.set_unusable_password()
            user.save()
            profile = Profile.objects.create(user=user)

            reset_form = PasswordResetForm({"email": email})
            if reset_form.is_valid():
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='password_reset_email.html',
                )

            messages.success(request, f"User {email} created and password reset email sent.")
            return redirect('admin_create_user')

#            login(request, user)
#            return redirect("profile")
    else:
        form = UserCreationForm()    
    
    return render(request, 'admin_create_user.html', {"form": form})



@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, "userprofile.html", {"profile": profile})