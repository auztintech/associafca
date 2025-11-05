from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('images/', views.ImageListCreateView.as_view(), name='image-list-create'),
    
]