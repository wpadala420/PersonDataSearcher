#!C:\Users\wpadala\PycharmProjects\PersonDataSearcher\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'instagramPictures==1.3.1','console_scripts','instagramPictures'
__requires__ = 'instagramPictures==1.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('instagramPictures==1.3.1', 'console_scripts', 'instagramPictures')()
    )
