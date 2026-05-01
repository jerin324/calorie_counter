from django.urls import path
from Calorie.views import *


urlpatterns = [
    path('register/',register_page,name='register_page'),
    path('',login_page,name='login_page'),
    path('dashboard/',dashboard, name='dashboard'),
    path('profile_page/',profile_page,name='profile_page'),
    path('profile-update/',profile_update,name='profile_update'),
    path('logout/',logout_page,name='logout_page'),
    
    path('daily-calories/',daily_consumed_list,name='daily_calories'),
    path('add_calorie/',add_calorie,name='add_calorie'),
    path('update-calorie/<int:id>/',update_calorie, name='update_calorie'),
    path('delete-calorie/<int:id>/',delete_calorie, name='delete_calorie'),
]
