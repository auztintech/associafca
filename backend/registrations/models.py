from django.db import models
from django.core.validators import RegexValidator

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='lgas')
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"


class PlayerRegistration(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    POSITION_CHOICES = [
        ('Goalkeeper', 'Goalkeeper'),
        ('Defender', 'Defender'),
        ('Midfielder', 'Midfielder'),
        ('Forward', 'Forward'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    GENOTYPE_CHOICES = [
        ('AA', 'AA'),
        ('AS', 'AS'),
        ('AC', 'AC'),
        ('SS', 'SS'),
        ('SC', 'SC'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # SECTION A: PLAYER INFORMATION
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100, default='Nigerian')
    residential_address = models.TextField()
    state_of_origin = models.ForeignKey(
        State, 
        on_delete=models.PROTECT, 
        related_name='players'
    )
    lga = models.ForeignKey(
        LGA, 
        on_delete=models.PROTECT, 
        related_name='players'
    )
    languages_spoken = models.CharField(max_length=200)
    preferred_position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    
    # SECTION B: EDUCATIONAL BACKGROUND
    current_school = models.CharField(max_length=200, blank=True, null=True)
    current_class = models.CharField(max_length=50, blank=True, null=True)
    highest_qualification = models.CharField(max_length=200, blank=True, null=True)
    
    # SECTION C: HEALTH & MEDICAL INFORMATION
    has_medical_condition = models.BooleanField(default=False)
    medical_condition_details = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    genotype = models.CharField(max_length=2, choices=GENOTYPE_CHOICES)
    has_physical_disability = models.BooleanField(default=False)
    physical_disability_details = models.TextField(blank=True, null=True)
    
    # SECTION D: PARENT/GUARDIAN INFORMATION
    parent_full_name = models.CharField(max_length=200)
    parent_relationship = models.CharField(max_length=50)
    parent_phone = models.CharField(validators=[phone_regex], max_length=17)
    parent_alternative_phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    parent_email = models.EmailField()
    parent_home_address = models.TextField(blank=True, null=True)
    
    # SECTION E: EMERGENCY CONTACT
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    
    # SECTION F: CONSENT & DECLARATION
    consent_participate = models.BooleanField(default=False)
    consent_information_accurate = models.BooleanField(default=False)
    consent_liability_release = models.BooleanField(default=False)
    consent_abide_rules = models.BooleanField(default=False)
    parent_signature = models.CharField(max_length=200)  # Can be replaced with image field
    player_signature = models.CharField(max_length=200, blank=True, null=True)
    submission_date = models.DateField(auto_now_add=True)
    
    # FOR OFFICIAL USE ONLY
    registration_number = models.CharField(max_length=50, unique=True, editable=False)
    date_received = models.DateTimeField(auto_now_add=True)
    approved_by = models.CharField(max_length=200, blank=True, null=True)
    medical_clearance = models.BooleanField(default=False)
    official_comments = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date_received']
    
    def save(self, *args, **kwargs):
        if not self.registration_number:
            # Generate unique registration number
            last_reg = PlayerRegistration.objects.all().order_by('id').last()
            if last_reg:
                last_id = last_reg.id
            else:
                last_id = 0
            self.registration_number = f"ASSOCIA-{last_id + 1:06d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} - {self.registration_number}"