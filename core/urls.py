from django.urls import path
from . import views
# urlpatterns here

urlpatterns = [
    path('', views.home, name='home')
]
