#!C:\Users\ruben\PycharmProjects\calibre-dump\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'shodan==1.22.0','console_scripts','shodan'
__requires__ = 'shodan==1.22.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('shodan==1.22.0', 'console_scripts', 'shodan')()
    )
