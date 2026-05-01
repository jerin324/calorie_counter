from django.contrib.auth.models import User
from Calorie.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class LoginForm(AuthenticationForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'
        exclude = ['user','bmr']
        
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
            'weight':forms.NumberInput(attrs={'class':'form-control','step': '0.01'}),
            'height':forms.NumberInput(attrs={'class':'form-control','step': '0.01'}),
            'bmr':forms.NumberInput(attrs={'class':'form-control','step': '0.01'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
        }

class ConsumedCalorieForm(forms.ModelForm):
    class Meta:
        model = ConsumedCaloryModel
        fields = '__all__'
        exclude = ['user','date']
        
        widgets = {
            'item_name':forms.TextInput(attrs={'class':'form-control'}),
            'calory':forms.NumberInput(attrs={'class':'form-control','step': '0.01'}),
        }