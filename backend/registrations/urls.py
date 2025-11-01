from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StateViewSet, LGAViewSet, PlayerRegistrationViewSet

router = DefaultRouter()
router.register(r'states', StateViewSet, basename='state')
router.register(r'lgas', LGAViewSet, basename='lga')
router.register(r'registrations', PlayerRegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
]
