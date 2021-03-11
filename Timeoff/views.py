from django.shortcuts import render, get_object_or_404
from .models import Timeoff
from .forms import TimeoffForm
# Create your views here.

# def timeoff_create_view(req):
#     my_form = RawProductForm()
#     if req.method == "POST":
#         my_form = RawProductForm(req.POST)
#         if my_form.is_valid():
#             #now data is good
#             print(my_form.cleaned_data)
#             Timeoff.objects.create(**my_form.cleaned_data)
#         else:
#             print(my_form.errors)
#     context = {
#         'form' : my_form
#     }
#     return render(req, "timeoffs/timeoff_create.html", context)

# def timeoff_create_view(req):
#     # print(req.GET)
#     # print(req.POST)
#     new_title = req.POST.get('title')
#     print(new_title)
#     context = {}
#     return render(req, "timeoffs/timeoff_create.html", context)

def timeoff_list_view(req):
    queryset = Timeoff.objects.all() # list of objects
    context = {
        "objec_list" : queryset
    }
    return render(req, "timeoffs/timeoff_list.html", context)

def timeoff_delete_view(req, myid):
    obj = get_object_or_404(Timeoff, id=myid)
    #POST request
    if req.method == 'POST':
        obj.delete()
    context = {
        "object": obj
    }
    return  render(req, "timeoffs/timeoff_delete.html", context)

def dynamic_lookup_view(req, myid):
    obj = get_object_or_404(Timeoff, id=myid)
    obj = Timeoff.objects.get(id=myid)
    context = {
        "objec" : obj
    }
    return render(req, "timeoffs/timeoff_detail.html", context)

# def render_initial_data(req):
#     initial_data = {
#         "title" : "Good title"
#     }
#     obj=Timeoff.objects.get(id=14)
#     form = TimeoffForm(req.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#     context = {
#         "form" : form
#     }
#     return render(req, "timeoffs/timeoff_create.html", context)

def timeoff_create_view(req):
    form = TimeoffForm(req.POST or None)
    if form.is_valid():
        form.save()
        form = TimeoffForm()
    context = {
        "form" : form
    }
    return render(req, "timeoffs/timeoff_create.html", context)

# def timeoff_detail_view(req):
#     obj = Timeoff.objects.get(id=12)
#     context = {"object" : obj
#     }
#     return render(req,"timeoffs/timeoff_detail.html",context)