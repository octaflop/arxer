# -*- encoding: utf-8 -*-
from __future__ import with_statement

from fabric.api import run, sudo, env, local, cd, prefix, settings
from contextlib import contextmanager as _contextmanager
import os, sys

DIR = os.path.abspath(os.path.dirname(__file__))
TMP = os.path.abspath('/tmp')

settings = {
    'project': 'arxer',
    'tmp': TMP,
    'dir': DIR,
}

env.hosts = ['cortex.local']
env.user = 'faris'
env.keyfile = ['$HOME/.ssh/id_rsa']
env.directory = DIR
env.activate = 'source %s/bin/activate' % DIR

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

# internal scripts
# packaging
def freeze():
    '''
    pip freeze all requirements into a local file
    '''
    with virtualenv():
        run('pip freeze --local > requirements.txt')

def pack():
    '''
    pack the entire project into a tar file
    '''
    local('tar czf /tmp/arxer.tgz .')


# depackaging
def dpkg():
    '''
    update pip and virtualenv
    install reqs based on requirements files
    '''
    with virtualenv():
        run('pip install -U pip')
        run('pip install -U virtualenv')
        with cd("%s/.." % DIR):
            run('virtualenv arxer')
        run('pip install -r arxer/requirements/project.txt')
        run('pip install -r requirements.txt')

# deployment
# install nginx

# install memcached

# install postgresql?

# vcs

# sanity check: check and see if the site runs after deployment

# testing
def test():
    '''
    test verbena and rose, the modified apps
    '''
    apps = [
        'verbena',
        'rose',
    ]
    with settings(warn_only=True):
        with virtualenv():
            with cd("%s/arxer" % DIR):
                for app in apps:
                    result = run('./manage.py test %s' % app)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at request of user")
    else:
        from prettyprint import pp
        pp(result)

def testall():
    '''
    test all included django apps
    '''
    with virtualenv():
        with cd("%s/arxer" % DIR):
            run('./manage.py test')

# resetall → nuke the server
def resetall():
    '''
    nukes the local sqlite database and reinstalls sync, fixtures, and
    migrations
    '''
    fixtures = [
        "flatpages",
        "sites",
        "chunks",
        "photologue",
    ]
    with cd("%s/arxer" % DIR):
        run("rm dev.db")
    with virtualenv():
        with cd("%s/arxer" % DIR):
            run('./manage.py syncdb')
            run('./manage.py migrate')
            for fix in fixtures:
                run('./manage.py loaddata apps/verbena/fixtures/%s.json' % fix)

def prepare_deploy():
    test()
    pack()

def deploy():
    '''
    the main deployment function
    '''
    pass

# main scripts
def dev():
    '''
    main DEV script for development environment.
    deploys all dev settings and starts a dev server
    '''
    with virtualenv():
        run('pip freeze --local')

def prod():
    '''
    main production script for production environment
    deploys production settings including:
        - caching
        - asset-smooshing
        - postgresql db
        - gunicorn
        - nginx:
            - static server
            - upstream server (reverse proxy)
    '''
    pass


