"""
WSGI config for prarabdha_jyotish project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prarabdha_jyotish.settings')

application = get_wsgi_application()

# Vercel looks for 'app' by default
app = application
