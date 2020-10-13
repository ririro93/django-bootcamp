from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from .forms import ProductModelForm
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

## 1
# def product_create_view(request, *args, **kwargs):
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             print("my_form: ", my_form)
#             print(my_form.is_valid())
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_form_input = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_form_input)
#                 print("post_data: ", post_data)
#     return render(request, "forms.html", {})

## 2
# def product_create_view(request, *args, **kwargs):
#     form = ProductForm(request.POST or None) # POST 면 선언하고 GET이면 None 넣고
#     if form.is_valid():
#         print(form.cleaned_data)
#         data = form.cleaned_data
#         Product.objects.create(**data)
#         form = ProductForm()
#         # return HttpResponseRedirect('/successs')
#     return render(request, "forms.html", {"form": form})

@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None) # POST 면 선언하고 GET이면 None 넣고
    if form.is_valid():
        obj = form.save(commit=False)
        # do something
        obj.user = request.user
        obj.save()
        form = ProductModelForm()
    return render(request, "forms.html", {"form": form})

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
    