"""
ASGI config for Autohaus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

#ist die Einstiegsdatei für ASGI-Server. Sie stellt deine Django-Anwendung so bereit, dass ein ASGI-kompatibler Server sie ausführen kann.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Autohaus.settings')

application = get_asgi_application()
