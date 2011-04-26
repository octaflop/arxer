from fabric import *
REPOS = (("arxer", "origin", "master"),)

def staging():
    config.fab_hosts = ['pineal.local']
    config.repos = REPOS

def git_pull():
    "Updates the repo"
    run("cd ~/workspace/projects/$(repo)/; git pull $(parent) $(branch)")

def git_reset():
    "Reset repo to specified version"
    run("cd ~/workspace/projects/$(repo)/; git reset --hard $(hash)")

def git_clone():
    "Clone a new repository"
    run("cd ~/workspace/projects/$(repo)/; git clone\
    git@amygdala.servebeer.com:arxer.git")

def reboot():
    "reset nginx"
    sudo("service nginx restart")

def pull():
    require("fab_hosts", provided_by=[staging])
    for repo, parent, branch in config.repos:
        config.repo = repo
        config.parent = parent
        config.branch = branch
        invoke(git_pull)

def clone():
    require("fab_hosts", provided_by=[staging])
    for repo, parent, branch in config.repos:
        config.repo = repo
        config.parent = parent
        config.branch = branch
        invoke(git_clone)

def reset(repo, hash):
    "reset all git repos to sepcific hash"
    require("fab_hosts", provided_by=[staging])
    config.hash = hash
    config.repo = repo
    invoke(git_reset)
