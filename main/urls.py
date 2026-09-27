from django.urls import path
from .views import (
    MerchantListView,
    LocationListAPIView,
    CategoryListAPIView,
    LogoListAPIView,
    FeedPostListView,
)

urlpatterns = [
    path('merchants/', MerchantListView.as_view(), name='merchant-list'),
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('logos/', LogoListAPIView.as_view(), name='logo-list'),
    path('feed/', FeedPostListView.as_view(), name='feed-post-list'),
]
