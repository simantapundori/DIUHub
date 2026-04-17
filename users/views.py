from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


# ===============================
# REGISTER
# ===============================
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "✅ Account created successfully!")

            return redirect('dashboard')
        else:
            messages.error(request, "❌ Please fix the form correctly.")

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ===============================
# LOGIN
# ===============================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "✅ Login successful!")

            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid username or password")

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# ===============================
# LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    messages.info(request, "👋 Logged out successfully")
    return redirect('login')


# ===============================
# DASHBOARD
# ===============================
@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


# ===============================
# PROFILE
# ===============================
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

<<<<<<< Updated upstream
=======
        messages.success(request, "✅ Profile updated successfully")

        return redirect('profile')

>>>>>>> Stashed changes
    return render(request, "users/profile.html", {"user": user})