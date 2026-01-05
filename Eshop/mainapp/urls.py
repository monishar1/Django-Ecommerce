from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeview),
    path('about/', views.aboutview),
    path('contact/', views.contactview)
]
