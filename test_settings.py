from flamenco.settings import *

INSTALLED_APPS.append(
    'werkzeug_debugger_runserver',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
