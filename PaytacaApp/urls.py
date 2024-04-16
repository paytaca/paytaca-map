from django.urls import path
from .views import LocationListAPIView, LogoListAPIView

urlpatterns = [
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('logos/', LogoListAPIView.as_view(), name='logo-list'),
]
