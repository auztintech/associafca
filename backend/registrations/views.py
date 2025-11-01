from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import State, LGA, PlayerRegistration
from .serializers import (
    StateSerializer, StateListSerializer, LGASerializer,
    PlayerRegistrationSerializer, PlayerRegistrationCreateSerializer,
    PlayerRegistrationListSerializer
)


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for states.
    GET /api/states/ - List all states
    GET /api/states/{id}/ - Get state with LGAs
    """
    queryset = State.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StateListSerializer
        return StateSerializer
    
    @action(detail=True, methods=['get'])
    def lgas(self, request, pk=None):
        """Get all LGAs for a specific state"""
        state = self.get_object()
        lgas = state.lgas.all()
        serializer = LGASerializer(lgas, many=True)
        return Response(serializer.data)


class LGAViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for LGAs.
    GET /api/lgas/ - List all LGAs
    GET /api/lgas/?state={state_id} - Filter LGAs by state
    """
    queryset = LGA.objects.all()
    serializer_class = LGASerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['state']
    search_fields = ['name']


class PlayerRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for player registrations.
    POST /api/registrations/ - Create new registration
    GET /api/registrations/ - List all registrations (admin only)
    GET /api/registrations/{id}/ - Get specific registration
    PUT/PATCH /api/registrations/{id}/ - Update registration (admin only)
    DELETE /api/registrations/{id}/ - Delete registration (admin only)
    """
    queryset = PlayerRegistration.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'state_of_origin', 'lga', 'preferred_position', 
                        'medical_clearance']
    search_fields = ['full_name', 'registration_number', 'parent_email']
    ordering_fields = ['date_received', 'full_name', 'age']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PlayerRegistrationCreateSerializer
        elif self.action == 'list':
            return PlayerRegistrationListSerializer
        return PlayerRegistrationSerializer
    
    def get_permissions(self):
        """
        Allow anyone to create registration
        Only admins can list, update, or delete
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create new player registration"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full details with registration number
        instance = PlayerRegistration.objects.get(pk=serializer.instance.pk)
        output_serializer = PlayerRegistrationSerializer(instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve a registration and grant medical clearance"""
        registration = self.get_object()
        registration.medical_clearance = True
        registration.approved_by = request.data.get('approved_by', 'Admin')
        registration.official_comments = request.data.get('comments', '')
        registration.save()
        
        serializer = PlayerRegistrationSerializer(registration)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Get registration statistics"""
        total = PlayerRegistration.objects.count()
        approved = PlayerRegistration.objects.filter(medical_clearance=True).count()
        pending = total - approved
        
        gender_stats = {}
        for choice in PlayerRegistration.GENDER_CHOICES:
            gender_stats[choice[0]] = PlayerRegistration.objects.filter(
                gender=choice[0]
            ).count()
        
        position_stats = {}
        for choice in PlayerRegistration.POSITION_CHOICES:
            position_stats[choice[0]] = PlayerRegistration.objects.filter(
                preferred_position=choice[0]
            ).count()
        
        return Response({
            'total_registrations': total,
            'approved': approved,
            'pending': pending,
            'by_gender': gender_stats,
            'by_position': position_stats
        })

