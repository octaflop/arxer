import pdb
pdb.set_trace()
from django.template import Template, Context

src =\
"""
    {% load nav_build %}{% sfpirgnavsub "oops" %}
"""

t = Template(src)

print t.render(Context({}))
