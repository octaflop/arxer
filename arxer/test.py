import pdb
pdb.set_trace()
from django.template import Template, Context

src1 = """
    {% load nav_build %}{% sfpirgnavsub "arx" %}
"""
src2 = """
    {% load nav_build %}{% sfpirgnavsub "rew" %}
"""
t = Template(src1)
t = Template(src2)

t.render(Context({}))
