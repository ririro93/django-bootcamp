from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

from .models import Product

# Create your views here.
# def bad_view(request, *args, **kwargs):
#     print(request.GET)
#     print(request.POST)
#     print(request.method)
#     my_request_data = dict(request.GET)
#     new_product = my_request_data.get("good")
#     print(my_request_data, new_product)
#     if new_product[0].lower() == "true":
#         print("new product")
#     return HttpResponse("don't do this")

def search_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World </h1>")
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"name": "junha", "query": "query"}
    return render(request, "home.html", context)

def product_create_view(request, *args, **kwargs):
    print(request.POST)
    print(request.GET)
    return render(request, "forms.html", {})

def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404
        
    # return HttpResponse(f"Product title is {obj.title}")
    return render(request, "products/detail.html", {"object":obj})

def product_api_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.pk})

def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)
    