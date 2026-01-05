from django.shortcuts import render

# Create your views here.


def homeview(request):
    template = 'mainapp/home.html'
    context = {}

    return render(request, template_name= template, context= context)

def aboutview(request):
    template = 'mainapp/about.html'
    context = {}

    return render(request, template_name= template, context= context)

def contactview(request):
    template = 'mainapp/contact.html'
    context = {}

    return render(request, template_name=template , context=context)
    