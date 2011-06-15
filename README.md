**Verbena** is a [public interest research group (“PIRG”)](http://en.wikipedia.org/wiki/Public_Interest_Research_Group) application for
*django*. It aims to allow PIRGS to organize projects, events, and researchers
around a centralized web platform.

No stable version has been released to date, but you can feel free to browse
the source.

# Installation:

Simply clone the repo and run:

````bash
python bootstrap.py
````

If you have issues, try manually installing:

````bash
virtualenv arxer
cd arxer
source bin/activate && cd arxer
pip install -r requirements/project.txt && pip install -r  ../requirements.txt
./manage.py syncdb && ./manage.py runserver
````

other required libraries include: django-filebrowser 3.3 -> this must be installed from the development svn branch. 

You will also need to copy the django-grappelli static files to the admin media. If running in development mode, you will need to manually add the django-grappelli files to the installation.

To enable search functionality, you will need to set up [solr](http://lucene.apache.org/solr/).

A full release with better documentation and branding is expected for June
2011.

