from django.db.models.signals import post_save
from verbena.models import Member
from pinax.apps.profiles.models import Profile
from django.contrib.auth.models import User, Permissions

# Perhaps not the best place for it, but here's a hook for creating a new
# member when a new user profile is created.

"""
def create_profile(sender, **kwargs):
"""
    """
    Create a new profile when a user object is saved
    Not implemented or used
    """
    """
    if not kwargs['created']:
        return
    user = kwargs['instance']
    try:
        p = Profile.objects.get(user=user)
        return p
    except Profile.DoesNotExist:
        p = None
    """

#post_save.connect(create_profile, sender=User)

def create_member(sender, **kwargs):
    """
    Create a new member when a User object is saved
    """
    # Check for a new user
    if not kwargs['created']:
        return

    # get the User account instance
    user = kwargs['instance']

    # don't make a member if it already exists
    try:
        p = Member.objects.get(profile=user)
        return p
    except Member.DoesNotExist:
        p = None
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(
            user = user,
        )
        profile.save()
    member = Member(
        profile = user,
    )
    member.save()

post_save.connect(create_member, sender=User)

def grant_addgroup_perms(sender, **kwargs):
    """
    Grant permission to faculty and students to create groups
    """
    user = kwargs['instance']
    perms = Permission.objects.get(codename='add_actiongroup')
    user.profile.user_permissions.add(perm)
    user.save()
    return user

"""
NOTES:
    Organizations cannot join workshops, they can only start arx projects
    Faculty doesn't do SHIT; they can join workshops
    Students can only create actiongroups
    all groups & projects must be approved in the admin interface and are
    classified in accordance to their approval status.
"""
post_save.connect(grant_addgroup_perms, sender=Student)
post_save.connect(grant_addgroup_perms, sender=Faculty)

def grant_arx_perms(sender, **kwargs):
    """
    Grant permission to organizations to manage arx:
        - add new project
        - delete their own project
    """
    user = kwargs['instance']
    perms = Permission.objects.get(codename='add_project')
    user.profile.user_permissions.add(perms)
    user.save()
    return user

post_save.connect(grant_arx_perms, sender=Organization)

