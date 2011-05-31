from verbena.models import Member
from django.db.models import Q

class MemberLookup(object):
    def get_query(self, q, request):
        """ Return a query set. request['user'] is important for filtering """
        return Member.objects.filter(Q(user__username__icontains=q))

    def format_result(self, member):
        """ Format the display for the dropdown menu """
        return u"%s %s %s (%s)" % (member.profile.user.first_name,
                member.user.last_name, member.profile.user.username,
                member.user.email)

    def format_item(self, member):
        """ Displays a formatted item in the area below the search box. """
        return unicode(member)

    def get_objects(self, ids):
        """ return a list of objects (this is used on m2m calls) """
        return Member.objects.filter(pk__in=ids).order_by('profile__user__first_name',
            'profile__user__last_name')

