"""
Env settings:
- sample_store__environment
- sample_store__secret_key
- sample_store__debug
"""

import os
from split_settings.tools import include
from pathlib import Path
import os
import random
import string
from os.path import dirname, abspath, basename
from logging import DEBUG as DEBUG_LOGGING

env = os.environ.get('sample_store__environment', 'local')

include('apps.py')
include(f'environments/{env}.py')

APPEND_SLASH = False
SITE_NAME = "Sample Store"

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('sample_store__secret_key', 'django-insecure-^xc8i^ha4-j7sk%l1qf3ox&#*cpx_!9ri^+e=yc#b1!9hlh$sa')

ALLOWED_HOSTS = ['*']
CART_ID = 'sample_store_cart'

SETTINGS_EXPORT = [
    'SITE_NAME',
    'DEBUG',
    'SITE_URL',
    'BASE_URL',
    'STATIC_URL',
    'STATIC_ROOT',
    'MEDIA_URL',
    'MEDIA_ROOT',
    'TEMPORARY_MEDIA'
]
