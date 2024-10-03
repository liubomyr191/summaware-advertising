"""Media_Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.http import HttpResponse

urlpatterns = [
	re_path(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow:", content_type="text/plain"), name="robots_file"),
	path('', include('Media_Manager.apps.Home.urls')),
	path('accounting/', include('Media_Manager.apps.Accounting.urls')),
	path('advertising/', include('Media_Manager.apps.Advertising.urls')),
	path('bi/', include('Media_Manager.apps.BI.urls')),
	path('circulation/', include('Media_Manager.apps.Circulation.urls')),
	path('editorial/', include('Media_Manager.apps.Editorial.urls')),
	path('login/', include('Media_Manager.apps.Home.urls')),
	path('forgot/', include('Media_Manager.apps.Home.urls')),
	path('logout/', include('Media_Manager.apps.Home.urls')),
	path('production/', include('Media_Manager.apps.Production.urls')),
	#path('admin/', include('Media_Manager.apps.Admin.urls')),
	path('admin/', admin.site.urls),
]
'''
if settings.ADMIN_ENABLED:
	urlpatterns += (path('admin/', admin.site.urls),)
else:
	urlpatterns += (path('admin/', include('Media_Manager.apps.Admin.urls'),)
'''
#handler404 = 'admin.views.error_404_view'