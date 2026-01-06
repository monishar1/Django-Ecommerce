from django.shortcuts import render

from .models import CarouselImage

# Create your views here.


def homeview(request):
    template = 'mainapp/home.html'
    context = {
        'current_page' : 'home',

        # Let's collect all exisiting records of carousel image table to be sent to template
        'carousel_images' : CarouselImage.objects.all() # Select * from carousel_image;
    }

    return render(request, template_name= template, context= context)

def aboutview(request):
    template = 'mainapp/about.html'
    context = {
        'current_page' : 'about'
    }

    return render(request, template_name= template, context= context)

def contactview(request):
    template = 'mainapp/contact.html'
    context = {
        'current_page' : 'contact'
    }

    return render(request, template_name=template , context=context)
    