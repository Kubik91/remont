#!/home/user2057107/iteh/www/env/scripts python
"""
Command-line utility for administrative tasks.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "remont.settings"
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
