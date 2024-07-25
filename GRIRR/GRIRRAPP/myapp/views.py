from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Login function
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'main/login.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def children(request):
    return render(request, 'main/children.html')

def program_costs(request):
    return render(request, 'main/program_costs.html')

def baselines(request):
    return render(request, 'main/baselines.html')

def toolkit(request):
    return render(request, 'main/toolkit.html')

def resources(request):
    return render(request, 'main/resources.html')
