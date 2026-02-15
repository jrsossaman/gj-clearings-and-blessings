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
    PERSON = "person"
    PET = "pet"

    SPECIES_TYPE_CHOICES = [
        (PERSON, "Person"),
        (PET, "Pet")
    ]
    
    MALE = "male"
    FEMALE = "female"

    GENDER_TYPE_CHOICES = [
        ("", "Select"),
        (MALE, "Male"),
        (FEMALE, "Female")
    ]

    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="clients")
    first_name=models.CharField(max_length=15, null=True, validators=[letters_only])
    last_name=models.CharField(max_length=20, null=True, validators=[letters_only])
    person_or_pet=models.CharField(
        max_length=20,
        choices=SPECIES_TYPE_CHOICES,
        default="person"
    )
    species=models.CharField(max_length=20, blank=True, null=True, validators=[letters_only])
    gender=models.CharField(
        max_length=20,
        choices=GENDER_TYPE_CHOICES,
        blank=True,
        null=True,
        default=""
    )
    email=models.EmailField(blank=True, null=True, unique=True)
    is_user=models.BooleanField(default=False, editable=False)
    is_active=models.BooleanField(default=True, editable=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.profile and self.profile.clients.filter(is_user=True).exists():
                self.is_user=False
            else: self.is_user=True
        super(Client, self).save(*args, **kwargs)



class Location(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, related_name="locations_by_client", null=True, blank=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="locations_by_profile", null=True, blank=True)
    street=models.CharField(max_length=20, null=True)
    street_ext=models.CharField(max_length=10, null=True, blank=True)
    city=models.CharField(max_length=20, null=True, validators=[letters_only])
    state=models.CharField(max_length=20, null=True, validators=[letters_only])
    zip_code=models.CharField(max_length=10, null=True, validators=[numbers_only])
    country=models.CharField(max_length=50, null=True, validators=[letters_only])

    def __str__(self):
        street_ext = f", {self.street_ext}" if self.street_ext else ""
        return f"{self.street} {street_ext}, {self.city}, {self.state} {self.zip_code} {self.country}"
    


########## Session Sheet Stuff ###############

OPEN = "open"
CLOSED_TO_OPEN = "closed_to_open"
SEE_NOTES = "see_notes"

CHAKRAS_TYPE_CHOICES = [
    (OPEN, "Open"),
    (CLOSED_TO_OPEN, "Closed > Open"),
    (SEE_NOTES, "See Notes"),
]

DARK_ENTITIES = "dark_entities"
ATTACKS = "attacks"
SOCIETAL = "societal"
VIRUSES = "viruses"

HINDRANCE_TYPE_CHOICES = [
    (DARK_ENTITIES, "Dark Entities"),
    (ATTACKS, "Attacks"),
    (SOCIETAL, "Societal"),
    (VIRUSES, "Viruses")
]

class Session_Sheet(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, related_name="session_sheets")

    date=models.DateField()

    spiritual1=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    mental1=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    emotional1=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    physical1=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    
    chakras=models.CharField(
        max_length=20,
        choices=CHAKRAS_TYPE_CHOICES,
        default="open"
    )
    cords=models.BooleanField(default=False)
    how_many=models.CharField(
        max_length=10,
        validators=[numbers_only],
        blank=True,
        null=True
    )
    to_whom=models.CharField(
        max_length=999,
        validators=[numbers_only],
        blank=True,
        null=True
    )
    hindrances=models.CharField(
        max_length=200,
        blank=True,
        choices=HINDRANCE_TYPE_CHOICES,
        default=""
    )
    
    spiritual2=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    mental2=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    emotional2=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    physical2=models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)])
    
    notes=models.TextField(null=True, blank=True)
    
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
    
    @property
    def get_hindrances_list(self):
        return self.hindrances.split(',')

    @property
    def set_hindrances_list(self, hindrances):
        self.hindrances = ",".join(hindrances)
    


UNWANTED_ENERGIES = "unwanted_energies"
STUCK_SOULS = "stuck_souls"
PORTALS = "portals"

ISSUES_TYPE_CHOICES = [
    (UNWANTED_ENERGIES, "Unwanted Energies"),
    (STUCK_SOULS, "Stuck Souls"),
    (PORTALS, "Portals")
]

class Location_Sheet(models.Model):

    address=models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location_sheets")

    date=models.DateField()

    issues=models.CharField(
        max_length=200,
        blank=True,
        choices=ISSUES_TYPE_CHOICES,
        default=""
        )
    protection=models.BooleanField(default=False)

    @property
    def get_issues_list(self):
        return self.issues.split(',')

    @property
    def set_issues_list(self, issues):
        self.issues = ",".join(issues)

    notes=models.TextField(null=True, blank=True)