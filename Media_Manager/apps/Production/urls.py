from django.urls import path

from . import views

urlpatterns = [
	path('', views.production_view, name='production_view'),
]