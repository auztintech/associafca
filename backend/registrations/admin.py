from django.contrib import admin
from .models import PlayerRegistration



@admin.register(PlayerRegistration)
class PlayerRegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'gender', 'age', 
                    'state_of_origin', 'preferred_position', 'medical_clearance', 
                    'date_received']
    list_filter = ['gender', 'preferred_position', 'medical_clearance', 
                   'state_of_origin', 'date_received']
    search_fields = ['full_name', 'registration_number', 'parent_email', 
                     'parent_phone']
    
    readonly_fields = ['registration_number', 'date_received', 'submission_date']
    
    fieldsets = (
        ('Registration Info', {
            'fields': ('registration_number', 'date_received')
        }),
        ('Player Information', {
            'fields': ('full_name', 'date_of_birth', 'age', 'gender', 
                      'nationality', 'residential_address', 'state_of_origin', 
                      'lga', 'languages_spoken', 'preferred_position')
        }),
        ('Educational Background', {
            'fields': ('current_school', 'current_class', 'highest_qualification'),
            'classes': ('collapse',)
        }),
        ('Health & Medical Information', {
            'fields': ('has_medical_condition', 'medical_condition_details', 
                      'blood_group', 'genotype', 'has_physical_disability', 
                      'physical_disability_details')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_full_name', 'parent_relationship', 'parent_phone', 
                      'parent_alternative_phone', 'parent_email', 'parent_home_address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 
                      'emergency_contact_relationship'),
            'classes': ('collapse',)
        }),
        ('Consent & Declaration', {
            'fields': ('consent_participate', 'consent_information_accurate', 
                      'consent_liability_release', 'consent_abide_rules', 
                      'parent_signature', 'player_signature', 'submission_date')
        }),
        ('Official Use Only', {
            'fields': ('approved_by', 'medical_clearance', 'official_comments'),
            'classes': ('collapse',)
        }),
    )
