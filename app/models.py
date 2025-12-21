from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def primary_client(self):
        return self.clients.get(is_user=True)
    


class Client(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="clients")
    first_name=models.CharField(max_length=15, null=True)
    last_name=models.CharField(max_length=20, null=True)
    email=models.EmailField(blank=True, null=True, unique=True)
    is_user=models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.profile and self.profile.clients.filter(is_user=True).exists():
                self.is_user=False
            else: self.is_user=True
        super(Client, self).save(*args, **kwargs)

        

class Session_Sheet(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    client=models.ForeignKey(Client, on_delete=models.CASCADE)

    date=models.DateField()

    spiritual1=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    mental1=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    emotional1=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    physical1=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    chakras=models.BooleanField(default=False)
    cords=models.BooleanField(default=False)
    hinderances=models.BooleanField(default=False)
    dark_entities=models.BooleanField(default=False)
    attacks=models.BooleanField(default=False)
    social=models.BooleanField(default=False)
    viruses=models.BooleanField(default=False)
    
    spiritual2=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    mental2=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    emotional2=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    physical2=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    @property
    def total1(self):
        return self.spiritual1 + self.mental1 + self.emotional1 + self.physical1
    
    @property
    def total2(self):
        return self.spiritual2 + self.mental2 + self.emotional2 + self.physical2
    
    @property
    def percent_change(self):
        if self.total1 == 0:
            return None
        return ((self.total1 - self.total2) / self.total1) * 100
    
