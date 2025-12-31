from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
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
                if user.is_staff:
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


################################################################################################################


def create_admin_user(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_staff=True
        user.save()
        login(request, user)
        return HttpResponse("Admin user created successfully!")
    return render(request, 'create_admin_user.html')
# Set CSRF_COOKIE_SECURE = False at the bottom of settings. Reset to True before launch.


def is_admin(user):
    return user.is_staff


User = get_user_model()
@login_required
@user_passes_test(is_admin)
def admin_user_creation(request):  
    if request.method == "POST":
        client_form = PrimaryClientCreationForm(request.POST)
        user_form = UserCreationForm(request.POST)
        if client_form.is_valid() and user_form.is_valid():
            email=user_form.cleaned_data["email"]
            password=user_form.cleaned_data["password"] # Delete this field for production. Will be handled by user.set_unusable_password() below.

            user = User.objects.create_user(username=email, email=email, password=password) # Delete password=password for production. Added here for testing.
#            user.set_unusable_password() # This will enable user-created passwords on password reset
            user.save()

            profile = Profile.objects.create(user=user)
            profile.save()

            client = client_form.save(commit=False)#Client.objects.create(profile=profile, first_name=None, last_name=None, email=user.email, is_user=True)
            client.profile = profile
            client.email = email
            if not profile.clients.exists():
                client.is_user=True
            else:
                client.is_user=False
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
        client_form = PrimaryClientCreationForm()
        user_form = UserCreationForm()    
    
    return render(request, 'admin_create_user.html', {"client_form": client_form, "user_form": user_form})


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    selected_client = None
    selected_client_id = request.session.get('selected_client')  # Get client ID from session

    if selected_client_id:
        try:
            selected_client = Client.objects.get(id=selected_client_id)  # Fetch the client object
        except Client.DoesNotExist:
            selected_client = None  # In case the client is deleted or invalid

    if request.method == "POST":
        form = ClientSelectForm(request.POST)
        if form.is_valid():
            selected_client = form.cleaned_data["client"]
            request.session['selected_client'] = selected_client.id  # Store client ID in session
            return redirect('admin_dashboard')  # Reload to reflect the new selection
    else:
        # If there's a selected client, initialize the form with that client object
        form = ClientSelectForm(initial={'client': selected_client}) if selected_client else ClientSelectForm()

    return render(request, "admin_dashboard.html", {"form": form, "selected_client": selected_client})



@login_required
@user_passes_test(is_admin)
def admin_client_overview(request):
    selected_client = None
    selected_client_id = request.session.get('selected_client', None)
    if selected_client_id:
        selected_client = Client.objects.get(id=selected_client_id)
    return render(request, 'admin_client_overview.html', {'selected_client': selected_client})



@login_required
@user_passes_test(is_admin)
def create_session_sheet(request):
    selected_client_id = request.session.get('selected_client', None)
    if not selected_client_id:
        raise Http404("No client selected.")

    user_client = Client.objects.get(id=selected_client_id)
    clients = Client.objects.filter(profile=user_client.profile)

    if request.method == 'POST':
        form = SessionSheetForm(request.POST, clients_queryset=clients)
        if form.is_valid():
            session_sheet = form.save(commit=False)
            session_sheet.user = request.session.get('selected_client') # 'user_client' before
            session_sheet.save()
            return redirect('admin_prev_client_sessions')
    else:
        form = SessionSheetForm(clients_queryset=clients)

    return render(request, 'admin_new_session_sheet.html', {
        'form': form,
        'selected_client': user_client
    })




@login_required
@user_passes_test(is_admin)
def view_prevs_as_admin(request):
    selected_client = None
    selected_client_id = request.session.get('selected_client', None)
    if selected_client_id:
        selected_client = Client.objects.get(id=selected_client_id)

    # Get the USER-CLIENT from session (account owner)
    user_client_id = selected_client_id #request.session.get('selected_client')
    if not user_client_id:
        raise Http404("No client selected.")

    user_client = Client.objects.get(id=user_client_id)

    # All clients on this account (user + secondary)
    clients = Client.objects.filter(profile=user_client.profile)

    # Base queryset: ALL sessions for this profile
    session_sheets = Session_Sheet.objects.filter(
        client__profile=user_client.profile
    )

    # Filters
    client_filter = request.GET.get('client')
    date_filter = request.GET.get('date')

    if client_filter:
        session_sheets = session_sheets.filter(client_id=client_filter)

    if date_filter:
        session_sheets = session_sheets.filter(date=date_filter)

    session_sheets = session_sheets.order_by('-date')

    context = {
        'selected_client': selected_client,
        'user_client': user_client,           # account owner
        'clients': clients,                   # dropdown list
        'session_sheets': session_sheets,
        'client_filter': int(client_filter) if client_filter else None,
        'date_filter': date_filter,
    }

    return render(request, 'admin_prev_client_sessions.html', context)
#    selected_client = None
#    selected_client_id = request.session.get('selected_client', None)
#    if selected_client_id:
#        selected_client = Client.objects.get(id=selected_client_id)
#
#    user = request.user
#    if user.is_staff:
#        profile = getattr(user, 'profile', None)
#    else:
#        try:
#            profile = user.profile
#        except Profile.DoesNotExist:
#            raise Http404('Profile not found.')
#        
#    if selected_client:
#        clients = Client.objects.filter(profile=selected_client.profile)
#    else:
#        clients = Client.objects.none()
#
#    client_filter = None
#    date_filter = None
#    session_sheets = Session_Sheet.objects.none()
#
#    if request.method == 'GET':
#        client_filter=request.GET.get('client')
#        date_filter=request.GET.get('date')
#        if client_filter:
#            selected_client=Client.objects.get(id=client_filter)
#            session_sheets=session_sheets.filter(client=selected_client)
#        if date_filter:
#            session_sheets=session_sheets.filter(date=date_filter)
#    
#    session_sheets=session_sheets.order_by('-date')
#
#    context = {
#        'selected_client': selected_client,
#        'clients': clients,
#        'session_sheets': session_sheets,
#        'client_filter': client_filter,
#        'date_filter': date_filter
#    }
#
#    return render(request, 'admin_prev_client_sessions.html', context)



@login_required
@user_passes_test(is_admin)
def update_client_account(request):
    selected_client = None
    selected_client_id = request.session.get('selected_client', None)
    if selected_client_id:
        selected_client = Client.objects.get(id=selected_client_id)

    client_form = AdditionalClientCreationForm()

    if request.method == "POST":
        client_form = AdditionalClientCreationForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.profile = selected_client.profile
            client.is_user = False
            client.save()

    return render(request, 'admin_update_client_account.html', {'client_form': client_form, 'selected_client': selected_client})



@login_required
@user_passes_test(is_admin)
def delete_user_profile(request):
    return render(request, 'admin_delete_user_profile.html')



def reset_client_selection(request):
    if 'selected_client' in request.session:
        del request.session['selected_client']
    return redirect('admin_dashboard')