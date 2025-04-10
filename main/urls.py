from django.urls import path
from .views import MerchantListView, LocationListAPIView, CategoryListAPIView, LogoListAPIView

urlpatterns = [
    path('merchants/', MerchantListView.as_view(), name='merchant-list'),
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('logos/', LogoListAPIView.as_view(), name='logo-list'),
]
