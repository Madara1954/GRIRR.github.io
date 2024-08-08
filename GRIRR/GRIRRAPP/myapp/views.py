from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'main/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'main/login.html')

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

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
