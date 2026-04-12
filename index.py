import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prarabdha_jyotish.settings')
app = get_wsgi_application()
