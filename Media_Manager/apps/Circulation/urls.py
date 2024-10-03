from django.urls import path

from . import views

urlpatterns = [
	path('', views.circulation_view, name='circulation_view'),
]