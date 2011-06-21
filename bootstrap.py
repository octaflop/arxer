import os, sys, parser
import subprocess, shutil

import pip
if "VIRTUAL_ENV" not in os.environ:
    sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
    parser.print_usage()
    sys.exit(-1)

virtualenv = os.environ["VIRTUAL_ENV"]
file_path = os.path.dirname(__file__)
subprocess.call(["pip", "install", "-E", virtualenv, "--requirement",
                 os.path.join(file_path, "arxer/requirements/project.txt")])
subprocess.call(["pip", "install", "-E", virtualenv, "--requirement",
                 os.path.join(file_path, "requirements.txt")])
#old, uncomment this to revert to original paths
##FB_DOWNLOAD = "https://github.com/wardi/django-filebrowser-no-grappelli.git"
FB_DOWNLOAD = "git://github.com/octaflop/django-filebrowser-no-grappelli.git"

subprocess.call(["git", "clone", FB_DOWNLOAD, os.path.join(file_path,\
    "django-filebrowser")])
# build the source
subprocess.call(["python", os.path.join(file_path, "django-filebrowser",
    "setup.py"), "build"])
# makeshift install if needed
version = sys.version_info
# checks for version 2.6 or 2.7 (to determine filepath)
if version[1] == 6:
    version = "python2.6"
elif version[1] == 7:
    version = "python2.7"
else:
    raise
sp = os.path.join(file_path, "lib", version, "site-packages")

if not os.path.isdir(os.path.join(sp, "filebrowser")):
    shutil.copytree(os.path.join(file_path, "django-filebrowser", "filebrowser"),
        os.path.join(sp, "filebrowser"))

# Copy the filebrowser mediafiles to the static files location

if not os.path.isdir(os.path.join(file_path, "arxer", "site_media", "static", "filebrowser")):
    shutil.copytree(os.path.join(sp, "filebrowser", "media", "filebrowser"), 
        os.path.join(file_path, "arxer", "site_media", "static", "filebrowser"))

