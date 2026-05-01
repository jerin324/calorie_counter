from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone  
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Calorie.forms import *
from Calorie.models import *
from django.contrib.auth.models import User

def register_page(request):
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'User create successfully.')
            return redirect('login_page')
    form_data = RegisterForm()
    context = {
        'form_data': form_data
    }
    return render(request, 'register.html', context)

def login_page(request):
    if request.method == 'POST':
        form_data = LoginForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Logged-in Successfully.')
                return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid Credentials.')
    
    form_data = LoginForm()
    context = {
        'form_data': form_data
    }
    
    return render(request, 'login.html',context)

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    today_consumed = ConsumedCaloryModel.objects.filter(
        user = user,
        date = today
    ).aggregate(total_calory = Sum('calory'))['total_calory'] or 0
    
    try:
        req_calorie = request.user.user_profile.bmr
    except ProfileModel.DoesNotExist:
        req_calorie = 0
    
    if today_consumed == req_calorie:
        status = 'Normal'
    elif today_consumed > req_calorie:
        status = 'Weight Gaining'
    else:
        status = 'Losing Weight'
    
    
    context = {
        'today_consumed': today_consumed,
        'req_calorie': req_calorie,
        'status': status
    }
    
    
    return render(request, 'dashboard.html',context)
@login_required
def profile_page(request):
    profile, created = ProfileModel.objects.get_or_create(user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)
@login_required
def profile_update(request):
    user = request.user
    try:
        profile_data = ProfileModel.objects.get(user = user)
    except ProfileModel.DoesNotExist:
        profile_data = None
    if request.method == 'POST':
        form_data = ProfileUpdateForm(request.POST, instance=profile_data)
        if form_data.is_valid():
            profile_data = form_data.save(commit=False)
            if profile_data.gender == 'Male':
                bmr_data = Decimal(66.47) + (Decimal(13.75) * Decimal(profile_data.weight)) + (Decimal(5.003) * Decimal(profile_data.height)) - (Decimal(6.755) * Decimal(profile_data.age))
            else:
                bmr_data = Decimal(655.1) + (Decimal(9.563) * Decimal(profile_data.weight)) + (Decimal(1.850) * Decimal(profile_data.height)) - (Decimal(4.676) * Decimal(profile_data.age))
            profile_data.user = user
            profile_data.bmr = bmr_data
            profile_data.save()
            return redirect('profile_page')
                
    form_data = ProfileUpdateForm(instance=profile_data)
    context = {
        'form_data': form_data,
        'title': 'Profile Update',
        'btn_name': 'Update'
    }
    
    return render(request, 'master/base-form.html',context)
@login_required
def daily_consumed_list(request):
    calorie_data = ConsumedCaloryModel.objects.filter(user = request.user)
    
    context = {
        'calorie_data': calorie_data
    }

    return render(request, 'daily-consumed-list.html', context)
@login_required
def add_calorie(request):
    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('daily_calories')
    
    form_data = ConsumedCalorieForm()
    context = {
        'form_data': form_data,
        'title': 'Add Calorie',
        'btn_name': 'Add Calorie'
    }
    
    return render(request, 'master/base-form.html',context)
@login_required
def update_calorie(request, id):
    data = ConsumedCaloryModel.objects.get(id = id)
    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('daily_calories')
    
    form_data = ConsumedCalorieForm(instance=data)
    context = {
        'form_data': form_data,
        'title': 'Add Calorie',
        'btn_name': 'Add Calorie'
    }
    
    return render(request, 'master/base-form.html',context)
@login_required
def delete_calorie(request, id):
    ConsumedCaloryModel.objects.get(id = id).delete()
    return redirect('daily_calories')