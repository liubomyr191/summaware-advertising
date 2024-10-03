from django.shortcuts import render, redirect
from django.http import HttpResponse
from ... import views

url = "192.241.131.173:8000"
login_redirect = "/login/?next="

def admin(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "/")

	context = {"message":"", "groups": ', '.join(views.get_groups(request)), "menu": views.get_sidebar(request)}
	return render(request, "admin.html", context)
