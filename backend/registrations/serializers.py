from rest_framework import serializers
from .models import State, LGA, PlayerRegistration
from datetime import date


class LGASerializer(serializers.ModelSerializer):
    class Meta:
        model = LGA
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    lgas = LGASerializer(many=True, read_only=True)
    
    class Meta:
        model = State
        fields = ['id', 'name', 'capital', 'lgas']


class StateListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing states without LGAs"""
    class Meta:
        model = State
        fields = ['id', 'name', 'capital']


class PlayerRegistrationSerializer(serializers.ModelSerializer):
    state_of_origin_name = serializers.CharField(source='state_of_origin.name', read_only=True)
    lga_name = serializers.CharField(source='lga.name', read_only=True)
    calculated_age = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayerRegistration
        fields = '__all__'
        read_only_fields = ['registration_number', 'date_received']
    
    def get_calculated_age(self, obj):
        """Calculate age from date of birth"""
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def validate(self, data):
        """Custom validation"""
        # Validate that LGA belongs to the selected state
        if data.get('lga') and data.get('state_of_origin'):
            if data['lga'].state != data['state_of_origin']:
                raise serializers.ValidationError(
                    "Selected LGA does not belong to the selected state."
                )
        
        # Validate all consents are checked
        consent_fields = [
            'consent_participate',
            'consent_information_accurate',
            'consent_liability_release',
            'consent_abide_rules'
        ]
        for field in consent_fields:
            if not data.get(field, False):
                raise serializers.ValidationError(
                    f"All consent fields must be checked. Missing: {field}"
                )
        
        # Validate age matches date of birth
        if data.get('date_of_birth') and data.get('age'):
            today = date.today()
            calculated_age = today.year - data['date_of_birth'].year - (
                (today.month, today.day) < (data['date_of_birth'].month, data['date_of_birth'].day)
            )
            if calculated_age != data['age']:
                raise serializers.ValidationError(
                    f"Age provided ({data['age']}) does not match date of birth. Calculated age: {calculated_age}"
                )
        
        return data


class PlayerRegistrationCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating registrations"""
    class Meta:
        model = PlayerRegistration
        exclude = ['registration_number', 'date_received', 'approved_by', 
                   'medical_clearance', 'official_comments']


class PlayerRegistrationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing registrations"""
    state_of_origin_name = serializers.CharField(source='state_of_origin.name', read_only=True)
    lga_name = serializers.CharField(source='lga.name', read_only=True)
    
    class Meta:
        model = PlayerRegistration
        fields = ['id', 'registration_number', 'full_name', 'date_of_birth', 
                  'gender', 'state_of_origin_name', 'lga_name', 'preferred_position',
                  'date_received', 'medical_clearance']
