from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
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
                if user.is_superuser:
                    return redirect("admin_dashboard")
                else:
                    return redirect("profile")
            else:
                form.add_error(None, "Invalid email or password.")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, "user_profile.html", {"profile": profile})



def is_admin(user):
    return user.is_superuser

#@login_required
#@user_passes_test(is_admin)
def admin_dashboard(request):
    form = ClientSelectForm()
    selected_client = None
    if request.method == "POST":
        form = ClientSelectForm(request.POST)
        if form.is_valid():
            selected_client = form.cleaned_data["client"]
    return render(request, "admin_dashboard.html", {"form": form, "selected_client": selected_client})


User = get_user_model()
#@login_required
#@user_passes_test(is_admin)
def admin_user_creation(request):
  
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"] # Delete this field for production. Will be handled by user.set_unusable_password() below.

            user = User.objects.create_user(username=email, email=email, password=password) # Delete password=password for production. Added here for testing.
#            user.set_unusable_password() # This will enable user-created passwords on password reset
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            client = Client.objects.create(profile=profile, first_name=None, last_name=None, email=user.email, is_user=True)
            client.save()

            reset_form = PasswordResetForm({"email": email})
            if reset_form.is_valid():
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    email_template_name='password_reset_email.html',
                )

            messages.success(request, f"User {email} created and password reset email sent.")
            return redirect('admin_create_user')

    else:
        form = UserCreationForm()    
    
    return render(request, 'admin_create_user.html', {"form": form})


#@login_required
#@user_passes_test(is_admin)
def create_session_sheet(request):
    if request.method == 'POST':
        form = SessionSheetForm(request.POST)
        if form.is_valid():
            session_sheet = form.save(commit=False)
            session_sheet.save()
            return redirect('session_sheet_detail', pk=session_sheet.pk)
    else:
        form = SessionSheetForm()

    return render(request, 'session_sheet_detail.html', {'form': form})



#@login_required
def session_sheet_detail(request, pk):
    session_sheet = get_object_or_404(Session_Sheet, pk=pk)

    if request.user != session_sheet.user and not request.user.is_superuser:
        return redirect('profile')
    
    return render(request, 'session_sheet_detail.html', {'session_sheet': session_sheet})