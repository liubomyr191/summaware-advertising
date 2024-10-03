"""
WSGI config for Media_Manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/Dev_Media_Manager')
sys.path.append('/var/www/Dev_Media_Manager/Media_Manager')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Media_Manager.settings')

application = get_wsgi_application()
