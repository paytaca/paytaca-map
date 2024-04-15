from django.urls import path
from .views import LocationListAPIView

urlpatterns = [
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
]
