from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeview, name = 'home_page'),
    path('about/', views.aboutview, name = 'about_page'),
    path('contact/', views.contactview, name = 'contact_page')
]
