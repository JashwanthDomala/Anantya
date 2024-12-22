from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from base.models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import auth

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        post = 'cast'

        print(f"Received data: {username}, {firstname}, {lastname}, {password1}, {password2}, {phone_number}, {post}")

        # Check if all fields are filled
        if not all([username, firstname, lastname, password1, password2, phone_number, post]):
            return render(request, 'account/register.html', {'error': "All fields are required."})

        # Check if passwords match
        if password1 != password2:
            return render(request, 'account/register.html', {'error': "Passwords do not match."})

        # Check if password length is greater than 10
        if len(password1) > 10:
            return render(request, 'account/register.html', {'error': "Password cannot be longer than 10 characters."})

        # Validate phone number length is exactly 10 digits
        if len(phone_number) != 10 or not phone_number.isdigit():
            return render(request, 'account/register.html', {'error': "Phone number must be exactly 10 digits."})

        # Check if username or phone number already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'account/register.html', {'error': "Username already exists."})

        if UserProfile.objects.filter(phone_number=phone_number).exists():
            return render(request, 'account/register.html', {'error': "Phone number already exists."})

        # Create user
        user = User.objects.create_user(username=username, password=password1, first_name=firstname, last_name=lastname)
        print(f"User created: {user}")

        # Create user profile
        user_profile = UserProfile.objects.create(user=user, phone_number=phone_number, post=post)
        print(f"User profile created: {user_profile}")

        # Redirect to login page after successful registration
        return redirect('accounts:login')  
    else:
        return render(request, 'account/register.html')




def loginpage(request):
    if request.method == 'POST':
        # Retrieve and sanitize inputs
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Validate empty fields
        if not username or not password:
            return render(request, 'account/login.html', {
                'message': "Both username and password are required."
            })

        # Authenticate user
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            try:
                # Fetch user profile and their post type
                user_profile = UserProfile.objects.get(user=user)
                user_post = user_profile.post

                # Redirect based on user type
                if user_post in ['cast', 'admin']:
                    return redirect('base:index')  # Customize URL name as per your app
                else:
                    return redirect('base:index')  # Default redirect
            except UserProfile.DoesNotExist:
                # Log the issue if needed for debugging
                # e.g., logging.error(f"UserProfile not found for user {user.username}")
                return redirect('base:index')  # Default redirect for missing profile
        else:
            # Invalid credentials
            return render(request, 'account/login.html', {
                'message': "Invalid username or password."
            })

    # Render login page for GET requests
    return render(request, 'account/login.html')




def logoutpage(request):
    logout(request)  # Log out the user
    return redirect('accounts:login')  # Redirect to the login page after logging out
