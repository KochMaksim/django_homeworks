from django.shortcuts import render, redirect
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = str(request.GET.get("sort", 'pk'))           # Getting parameters 'sort'. Default 'pk' - primary_key
    # print(f'request.GET.get("sort"): {type(sort)}: {(sort)}')
    phone_objects = Phone.objects.order_by(sort)
    context = {"phones": phone_objects}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_objects = Phone.objects.all()
    # phone_context = [p for p in phone_objects if p.slug == slug]
    for p in phone_objects:
        if p.slug == slug:
            phone_context = p
            break
    # print(f'phone_context: {type(phone_context)}: {phone_context}')
    context = {'phone': phone_context}
    return render(request, template, context)
