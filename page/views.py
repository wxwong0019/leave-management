from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def homepage_view(req, *args, **kwargs):
	print(args, kwargs,req.user)
	#return HttpResponse("<h1>Hello HTere!</h1>") #string of HTML code
	return render(req, "home.html",{})

def about_view(req, *args, **kwargs):
	#return HttpResponse("<h1>yoyo</h1>")
	my_context = {
		"my_text": "This is about us",
		"my_num" : 999 ,
		"my_list": [12,34,56]
	}
	return render(req, "about.html",my_context)
