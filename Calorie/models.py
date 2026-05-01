from django.db import models
from django.contrib.auth.models import User

class ProfileModel(models.Model):
    GENDER_CHOICES = [
        ('Male','Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=200, null=True)
    age = models.PositiveIntegerField(null=True, help_text='age in year')
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='weight in kg')
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text='height in cm')
    bmr = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=12, null=True)
    
    def __str__(self):
        return f'{self.name}-{self.bmr}'
    
class ConsumedCaloryModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_calory')
    item_name = models.CharField(max_length=100, null=True)
    calory = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.item_name}-{self.calory}'