from django.shortcuts import render, redirect

from django.urls import reverse

from .models import Product


from .forms import ProductForm, ProductImageForm

# Create your views here.
def productsView(request):
    template = 'products/products.html'
    context = {
        'current_page' : 'Product',

        'products' : Product.objects.all()
    }

    return render(request, template_name=template, context=context)

    # search Products
from django.db.models import Q

from django.db.models import Q

def searchProducts(request):
    template = 'products/search_results.html'
    query = request.GET.get('q', '')

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query)
        )
    else:
        products = Product.objects.none()

    context = {
        'query': query,
        'products': products
    }

    return render(request, template, context)

# CRUD Operatinons using Generic class Based Views of Django

from django.views.generic import (CreateView, DetailView,
                                   UpdateView, DeleteView)
                                
# ListView has already been implement using a function above : productsView()
from django.contrib.auth.mixins import LoginRequiredMixin
class CreateProduct(CreateView):
    model = Product
    template_name = 'products/add_product.html'
    success_url = '/products/'
    form_class = ProductForm
    #redirection url for successful creation of resource
    
    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home_page')
        return super().get(request, *args, **kwargs)

from django.views.generic.edit import FormMixin
# This mixin provides ability to render forms from th 'form_class'
from .forms import ProductImageForm

class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'
    # Providing form class for Product Images
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})

    # Overriding the queryset to pre-fetch
    # and add the product images alongside products
    def get_queryset(self):
        return Product.objects.prefetch_related('images')

    def post(self, request, *args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            image = form.save(commit = False)
            image.product = self.object
            image.save()
            return  redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

   
class UpdateProduct(UpdateView):
    model = Product
    fields = '__all__'
  
    template_name = 'products/update_product.html'
    success_url = '/products/'

    def get_success_url(self):
        return reverse('product_details' , kwargs={'pk' :self.object.pk})

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/'



# Edit  Product Image
from .models import ProductImage

class EditProductImage(UpdateView):
    model = ProductImage
    template_name = 'products/image_edit.html'
    form_class = ProductImageForm
    context_object_name = 'image'
    
    def get_success_url(self):
        return reverse('product_details' , kwargs={'pk':self.object.product.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'products/image_del.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details' , kwargs={'pk':self.object.product.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context