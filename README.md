**Verbena** is a public interest research group ("PIRG") application for
*django*. It aims to allow PIRGS to organize projects, events, and researchers
around a centralized web platform.

No stable version has been released to date, but you can feel free to browse
the source.

# Installation:

Simply clone the repo and run:

````
    python bootstrap.py
````

If you have issues, try manually installing:
````
    virtualenv arxer
    cd arxer
    source bin/activate && cd arxer
    pip install -r requirements/project.txt && pip install -r  ../requirements.txt
    ./manage.py syncdb && ./manage.py runserver
````

To enable search functionality, you will need to set up [solr](http://lucene.apache.org/solr/).

A full release with better documentation and branding is expected for June
2011.

