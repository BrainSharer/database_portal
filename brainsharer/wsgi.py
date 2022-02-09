import os, sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/var/www/brainsharer')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainsharer.settings')
application = get_wsgi_application()
