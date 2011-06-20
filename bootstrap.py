import os, sys, parser
import subprocess, shutil
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
FB_DOWNLOAD = "https://github.com/wardi/django-filebrowser-no-grappelli.git"
subprocess.call(["git", "clone", FB_DOWNLOAD, os.path.join(file_path,\
    "django-filebrowser")])
# build the source
subprocess.call(["python", os.path.join(file_path, "django-filebrowser",
    "setup.py"), "build"])
# makeshift install if needed
if not os.path.isdir(os.path.join(file_path, "lib", "python2.6", "site-packages",
    "filebrowser")):
    shutil.copytree(os.path.join(file_path, "django-filebrowser", "filebrowser"),
        os.path.join(file_path, "lib", "python2.6", "site-packages",
        "filebrowser"))

# add custom settings file for pinax
if os.path.isfile(os.path.join(file_path, "lib", "python2.6",
    "site-packages", "filebrowser", "settings.py")):
    shutil.move(os.path.join(file_path, "lib", "python2.6", "site-packages",
    "filebrowser", "settings.py"), os.path.join(file_path, "lib", "python2.6",
    "site-packages", "filebrowser", "settings.py.back"))
shutil.copyfile(os.path.join(file_path, "arxer", "requirements",
    "settings.py"), os.path.join(file_path, "lib", "python2.6",
    "site-packages", "filebrowser", "settings.py"))
