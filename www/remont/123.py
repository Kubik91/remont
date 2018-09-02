import os
import posixpath

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

STATIC_ROOT = posixpath.join(*([os.path.sep] + BASE_DIR.split(os.path.sep) + ['static']))
print(STATIC_ROOT)
