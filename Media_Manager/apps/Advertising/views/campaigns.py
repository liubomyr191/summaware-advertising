from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User, Group, Permission
from django.utils.crypto import get_random_string

import logging
logger = logging.getLogger(__name__)

from .... import views

from time import gmtime, strftime

# url = '127.0.0.1:8070'
login_redirect = '/login/?next='

def adHome(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'campaign/campaigns-home.html')

def adDashboard(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'campaign/campaign-dashboard.html')