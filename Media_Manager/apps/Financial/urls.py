from django.urls import path

from . import views

urlpatterns = [
	path('', views.financial_home, name='financial_home'),
]