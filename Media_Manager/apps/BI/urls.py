from django.urls import path, re_path

from .views import *

urlpatterns = [
	path('', display.bi_view, name='bi_view'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/$', display.section_view, name='section_view'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/filter$', display.section_view, name='section_view'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/viewdashboard/(?P<id>\d+)/$', display.view_dashboard_view, name='view_dashboard_view'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/chart/$', editors.chart, name='chart'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/chart/(?P<id>\d+)/$', editors.chart, name='chart'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/dashboard/$', editors.dashboard, name='dashboard'),
	re_path(r'^(?P<section>(accounting|advertising|circulation|editorial|production|admin))/dashboard/(?P<id>\d+)/$', editors.dashboard, name='dashboard'),

	path('ajax/', ajax.ajax_dashboard, name='ajax_dashboard'),
	path('ajax/reset', ajax.reset, name='reset'),
	path('ajax/resort', ajax.resort, name='resort'),
	path('ajax/export', ajax.export, name='export'),
	path('ajax/toggle_filter', ajax.toggle_filter, name='toggle_filter'),
]