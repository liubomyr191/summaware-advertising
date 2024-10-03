from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User, Group, Permission

from django.utils.crypto import get_random_string
from .models import Confirmation_Code
from .models import Org_Meta
from ... import views

from time import gmtime, strftime

url = '127.0.0.1:8070'
login_redirect = '/login/?next='

def index_view(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')

	context = {'message':'', 'groups': ', '.join(views.get_groups(request)), 'menu': views.get_sidebar(request)}
	return render(request, 'home.html', context)


def login_view(request):
	if request.user.is_authenticated:
		return redirect('/')

	org_logo_url_request = Org_Meta.objects.filter(meta_key= request.META['HTTP_HOST'] + '_url')
	org_logo_url = ''
	if org_logo_url_request.count() > 0:
		org_logo_url = org_logo_url_request[0].meta_value

	context = {'title': 'Login', 'page': 'login', 'path':'login.html', 'message': '', 'logo_url': org_logo_url}
	if not request.POST:
		return render(request, context['path'], context)

	user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password',''))
	if user is None:
		context['message'] = 'Error: Incorrect username/password credentials!'
		return render(request, context['path'], context)

	if user.is_active:
		login(request, user)
		#return redirect(request.GET.get('next','/') + '/')
		return redirect('/')
	else:
		context['message'] = 'Error: User isn\'t active!'
		return render(request, context['path'], context)	

def forgot(request):
	if request.user.is_authenticated:
		return redirect('/')

	context = {'title': 'Forgot Password', 'page': 'forgot', 'path':'forgot.html', 'message': ''}
	email = request.POST.get('email', -1)
	if email != -1:
		email_exists = User.objects.filter(email=email)
		if email_exists.count() < 1:
			context['message'] = 'No user exists with that email! Please try again with a different email:'
		else:
			random_code = get_random_string(length=32)
			confirmation_code = Confirmation_Code(user_id=email_exists[0].id,time=strftime("%Y-%m-%d %H:%M:%S", gmtime()),code=str(random_code), status='Ready').save()
			html_message = render_to_string('mail_template.html', {'domain': request.META['HTTP_HOST'],'code': str(random_code)})
			plain_message = strip_tags(html_message)
			send_mail('Password Reset Code', plain_message,'noreply@linux.midtc.com',[str(email_exists[0].email)],fail_silently=False, html_message=html_message)
			context['message'] = 'You should recieve an email with further instructions on how to reset your password. If you don\'t see any emails within a few minutes, try checking your spam folder.'

	return render(request, context['path'], context)

def reset(request):
	if request.user.is_authenticated:
		return redirect('/')

	context = {'title': 'Reset Password', 'page': 'reset', 'path':'reset.html', 'message': '', 'type': ''}
	code = request.GET.get('code', -1)
	password = request.GET.get('password', -1)
	password_confirmation = request.GET.get('password_confirmation', -1)
	context['code'] = code

	if code != -1 and password != -1 and password == password_confirmation:
		confirmation_exists = Confirmation_Code.objects.filter(code=code, status='Ready')
		if confirmation_exists.count() < 1:
			context['message'] = 'Error while changing your password! No such confirmation code exists!'
		else:
			u = User.objects.get(id=confirmation_exists[0].user_id)
			if u:
				u.set_password(password)
				u.save()
				confirmation_exists.update(status='Finished')
				context['message'] = 'Success'
				context['type'] = 'success'
			else:
				context['message'] = 'No user exists with that email! Please try again with a different email:'
				context['type'] = 'fail'
	else:
		context['type'] = 'code'

	return render(request, context['path'], context)

def logout_view(request):
	if request is not None and request.user is not None and request.user.is_authenticated:
		logout(request)
	return redirect('/login/')

def support(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')

	context = {'message':'', 'groups': ', '.join(views.get_groups(request)), 'menu': views.get_sidebar(request)}
	return render(request, 'support.html', context)