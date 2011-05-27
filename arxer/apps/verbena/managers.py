from django.db import models

#class MemberManager(models.Manager):
#    """
#    Pulls up all members, but allows the Member to remain an abstract
#    """
#    def all_mems(self):
#        members = []
#        genmems = GeneralMember.objects.all()
#        orgs = Organization.objects.all()
#        for org in orgs:
#            members.append(org)
#        students = Student.objects.all()
#        for student in students:
#            members.append(student)
#        facultys = Faculty.objects.all()
#        for faculty in facultys:
#            members.append(faculty)
#        return members

class ProjectManager(models.Manager):
    """
    Returns approved projects
    """
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(approval_status="AP")

