from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Product, Category

def index(request):
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count+1
    context = {
        'products_count': Product.objects.count(),
        'visits_count': visits_count,
    }
    return render(request, 'jewellery/index.html', context=context)

def jewellery(request):
    return render(request, 'jewellery/jewellery.html', {'jewellery': Category.objects.all()})