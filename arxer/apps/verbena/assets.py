import os
from settings import STATIC_ROOT
from django_assets import Bundle, register

js_top = Bundle('verbena/js/modernizr-1.7.min.js',
                filters='jsmin', output='verbena/js/top.js')

js_bottom = Bundle(
                'verbena/js/*.js',
                filters='jsmin', output='verbena/js/bottom.js')

def make_css_bundle(media_root, dir):
    files = os.listdir(os.path.join(media_root, dir))
    files.sort()
    files = [os.path.join(dir, f) for f in files]
    return files

css_all = Bundle(
                'verbena/css/*.css',
                filters='cssmin', output='verbena/css/all.css')

register('js_top', js_top)
register('js_bottom', js_bottom)
register('css_all', css_all)
