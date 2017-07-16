"""
WSGI config for WebApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add your project directory to the sys.path
# project_home = os.path.join(BASE_DIR, 'WebApp/WebApp')
# if project_home not in sys.path:
#     sys.path.append(project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebApp.settings")

application = get_wsgi_application()
