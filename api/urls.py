from django.urls import path
from . import views

urlpatterns = [
    path('instagram_feed/', views.ig_feed, name='ig-feed'),
    path('display_orders/', views.display_orders, name='display-order'),
    path('subscribe/', views.subscribe_to_newsletter, name='subscribe'),
]
