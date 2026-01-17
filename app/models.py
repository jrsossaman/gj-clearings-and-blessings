from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Create your models here.

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def primary_client(self):
        return self.clients.get(is_user=True)
    


letters_only = RegexValidator(
    regex=r'^[a-zA-Z ]+$',
    message='This field may contain letters only.'
)

numbers_only = RegexValidator(
    regex=r'^[0-9]+$',
    message='This field may contain numbers only.'
)
    


class Client(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="clients")
    first_name=models.CharField(max_length=15, null=True, validators=[letters_only])
    last_name=models.CharField(max_length=20, null=True, validators=[letters_only])
    email=models.EmailField(blank=True, null=True, unique=True)
    is_user=models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.profile and self.profile.clients.filter(is_user=True).exists():
                self.is_user=False
            else: self.is_user=True
        super(Client, self).save(*args, **kwargs)



class Location(models.Model):
    RESIDENCE = "residence"
    BUSINESS = "business"

    LOCATION_TYPE_CHOICES = [
        (RESIDENCE, "Residence"),
        (BUSINESS, "Business")
    ]

    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="locations")
    location_type=models.CharField(
        max_length=20,
        choices=LOCATION_TYPE_CHOICES,
        default=RESIDENCE
    )
    street=models.CharField(max_length=20, null=True)
    street_ext=models.CharField(max_length=10, null=True, blank=True)
    city=models.CharField(max_length=20, null=True, validators=[letters_only])
    state=models.CharField(max_length=20, null=True, validators=[letters_only])
    zip_code=models.CharField(max_length=10, null=True, validators=[numbers_only])
    country=models.CharField(max_length=50, null=True, validators=[letters_only])

    def __str__(self):
        street_ext = f", {self.street_ext}" if self.street_ext else ""
        return f"{self.street} {street_ext}, {self.city}, {self.state} {self.zip_code} {self.country} ({self.location_type})"
    
        

class Session_Sheet(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, related_name="session_sheets")

    date=models.DateField()

    spiritual1=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    mental1=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    emotional1=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    physical1=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    
    chakras=models.BooleanField(default=False)
    cords=models.BooleanField(default=False)
    hinderances=models.BooleanField(default=False)
    dark_entities=models.BooleanField(default=False)
    attacks=models.BooleanField(default=False)
    social=models.BooleanField(default=False)
    viruses=models.BooleanField(default=False)
    
    spiritual2=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    mental2=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    emotional2=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    physical2=models.PositiveIntegerField(
        validators=[MaxValueValidator(100)])
    
    notes=models.TextField(null=True)
    
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
        return (self.total1 / self.total2) * 100
    


class Location_Sheet(models.Model):
    address=models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_sheets")

    date=models.DateField()

    issues=models.BooleanField(default=False)
    unwanted_energies=models.BooleanField(default=False)
    stuck_souls=models.BooleanField(default=False)
    portals=models.BooleanField(default=False)
    protection=models.BooleanField(default=False)

    notes=models.TextField(null=True, blank=True)