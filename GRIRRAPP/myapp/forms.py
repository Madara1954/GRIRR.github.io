from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Child

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'user_type', 'password1', 'password2']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'username', 'phone_number',]  

class ChildForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        input_formats=['%Y-%m-%d'],  # specify the expected input format
    )
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'dob', 'age', 'gender', 'address']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


