from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Register new user
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login after register
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# Login existing user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# Logout user
def logout_view(request):
    logout(request)
    return redirect('login')


# Temporary dashboard
def dashboard(request):
    return render(request, 'users/dashboard.html')

#Profile view and edit
@login_required
def profile_view(request):

    user = request.user

    if request.method == "POST":

        user.full_name = request.POST.get("full_name")
        user.student_id = request.POST.get("student_id")
        user.email = request.POST.get("email")
        user.contact_number = request.POST.get("contact_number")
        user.blood_group = request.POST.get("blood_group")
        user.department = request.POST.get("department")
        user.batch = request.POST.get("batch")
        user.section = request.POST.get("section")

        user.save()

    return render(request, "users/profile.html", {"user": user})