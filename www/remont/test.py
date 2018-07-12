import sys
import os

a = os.path.abspath(os.path.dirname(__file__))

import settings
q = settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'remont.settings')
w = os.environ
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'..'))
s = sys.path


BASE_DIR = os.path.dirname(__file__)


site_packages = os.path.abspath(BASE_DIR + 'env/Lib/site-packages/')