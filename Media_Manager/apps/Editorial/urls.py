from django.urls import path

from . import views

urlpatterns = [
	path('', views.editorial_view, name='editorial_view'),
]