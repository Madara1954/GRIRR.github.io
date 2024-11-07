from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CustomUserForm, ChildForm
from .models import CustomUser, Child
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import get_user_model

User = get_user_model()
# SMTP server credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'pandallamaa@gmail.com'
sender_password = 'bodr ctys mves luug'  # App password

def send_verification_email(receiver_email):
    # Generate a random 6-digit verification code
    verification_code = random.randint(100000, 999999)

    subject = "Your Verification Code"
    body = f"Your verification code is {verification_code}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Verification code sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send verification email: {e}")

    return verification_code  # Return the code after sending the email




def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Make user inactive until verified
            user.save()

            # Generate and send the verification code via email
            verification_code = send_verification_email(user.email)

            # Store the code and user_id in session for later verification
            request.session['verification_code'] = verification_code
            request.session['user_id'] = user.id

            # Redirect to the page where user inputs the code
            return redirect('verify_email_code')  # No token is needed
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def verify_email_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('verification_code') 
        if int(user_code) == request.session.get('verification_code'):
            user = get_object_or_404(User, id=request.session['user_id'])
            user.is_active = True  
            user.save()

            
            del request.session['verification_code']
            del request.session['user_id']

            return redirect('login')  
        else:
            return render(request, 'main/verify_code.html', {'error': 'Invalid verification code'})
    else:
        return render(request, 'main/verify_code.html')

def parent_dashboard(request):
    return render(request, 'main/parentDashboard.html')

def employee_dashboard(request):
    return render(request, 'main/employeeDashboard.html')

 
def children_view(request):
    print("children_view function called.")
    if request.method == 'POST':
        print("Received POST request:", request.POST)  
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            print("Child successfully saved:", child)  
            return redirect('children')  
        else:
            print("Form errors:", form.errors)  
    else:
        form = ChildForm()

    
    children_list = Child.objects.filter(parent=request.user)
    print(f"Children for user {request.user}: {children_list}")  

    return render(request, 'main/children.html', {'form': form, 'children_list': children_list})

@login_required
def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return JsonResponse({
                'success': True,
                'child': {
                    'first_name': child.first_name,
                    'last_name': child.last_name,
                    'age': child.age
                }
            })
        else:
            # Return errors if the form is not valid
            return JsonResponse({
                'success': False,
                'errors': [error for error in form.errors.values()]
            })
    else:
        form = ChildForm()

    children_list = Child.objects.filter(parent=request.user)
    return render(request, 'main/children.html', {'form': form, 'children_list': children_list})


def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == "POST":
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ChildForm(instance=child)
    return render(request, 'edit_child.html', {'form': form, 'child': child})




@login_required
def delete_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == 'POST':
        user_id = child.parent.id  
        child.delete()
        return redirect('children')


def logout_view(request):
    logout(request)
    return redirect('login')  

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  
        password = request.POST.get('password')
        print(f"Received POST data: {email}, {password}")  

        
        user = authenticate(request, username=email, password=password) 

        if user is not None:
            print("User authenticated successfully")
            print("Stored user_type:", user.user_type)
            login(request, user)

           
            if user.user_type == 'parent':
                return redirect('parentDashboard')
            elif user.user_type == 'employee':
                return redirect('employeeDashboard')
        else:
            print("User authentication failed")
            return render(request, 'main/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'main/login.html')
    pass
    
def user_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    children = Child.objects.filter(parent=user)
    print(f"Children for profile: {children}")  
    return render(request, 'user_profile.html', {'user': user, 'children': children})



def edit_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    children = Child.objects.filter(parent=user)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
    else:
        form = CustomUserForm(instance=user)
    
    return render(request, 'main/edit_profile.html', {'form': form, 'user': user, 'children': children})

def parent_details_view(request, parent_id):
    parent = get_object_or_404(CustomUser, id=parent_id)
    children = Child.objects.filter(parent=parent)
    return render(request, 'main/admin/parent_details.html', {
        'parent': parent,
        'children': children,
    })


@login_required
def children(request):
    return render(request, 'main/children.html')

@login_required
def program_costs(request):
    return render(request, 'main/program_costs.html')

@login_required
def baselines(request):
    return render(request, 'main/baselines.html')

@login_required
def toolkit(request):
    return render(request, 'main/toolkit.html')

@login_required
def resources(request):
    return render(request, 'main/resources.html')

@login_required
def parent_dashboard(request):
    return render(request, 'main/parentDashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'main/employeeDashboard.html')
