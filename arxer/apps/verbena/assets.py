import os
from settings import STATIC_ROOT
from django_assets import Bundle, register

js_top = Bundle('verbena/js/libs/modernizr-1.7.min.js',
                filters='jsmin', output='gen/top.js')

js_bottom = Bundle('verbena/js/libs/jquery-1.5.1.min.js',
                'verbena/js/libs/dd_belatedpng.js',
                'verbena/js/libs/jquery-ui.custom.min.js',
                'verbena/js/libs/jquery-ui-timepicker-addon.js',
                'verbena/js/libs/base.js',
                'verbena/js/map.js',
                'verbena/js/search.js',
                'verbena/js/ajax_select.js',
                filters='jsmin', output='gen/bottom.js')

def make_css_bundle(media_root, dir):
    files = os.listdir(os.path.join(media_root, dir))
    files.sort()
    files = [os.path.join(dir, f) for f in files]
    return files

css_all = Bundle('verbena/diversifist/css/sfpirg.css',
                'verbena/css/style.css',
                'verbena/diversifist/css/colors/about.css',
                'verbena/diversifist/css/colors/action.css',
                'verbena/diversifist/css/colors/arx.css',
                'verbena/diversifist/css/colors/front_page.css',
                'verbena/diversifist/css/colors/get_involved.css',
                'verbena/diversifist/css/colors/research.css',
                'verbena/css/iconic.css',
                #make_css_bundle(STATIC_ROOT, 'verbena/css'),
                #make_css_bundle(STATIC_ROOT, 'verbena/diversifist/css'),
                filters='cssmin', output='gen/all.css')

register('js_top', js_top)
register('js_bottom', js_bottom)
register('css_all', css_all)
