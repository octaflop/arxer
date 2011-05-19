import os
from settings import STATIC_ROOT
from django_assets import Bundle, register

js_top = Bundle('verbena/js/libs/modernizr-1.7.min.js',
                filters='jsmin', output='gen/top.js')

js_bottom = Bundle('verbena/js/libs/*.js',
                'verbena/js/*.js',
                'pinax/js/*.js',
                'tiny_mce/js/*.js',
                'uni_form/js/*.js',
                'filebrowser/js/*.js',
                'debug_toolbar/js/*.js',
                'ajax_validation/js/*.js',
                filters='jsmin', output='gen/bottom.js')

def make_css_bundle(media_root, dir):
    files = os.listdir(os.path.join(media_root, dir))
    files.sort()
    files = [os.path.join(dir, f) for f in files]
    return files

css_all = Bundle('verbena/diversifist/css/*.css',
                'verbena/css/*.css',
                'verbena/diversifist/css/colors/*.css',
                'verbena/css/iconic.css',
                'tribes/*.css',
                'tasks/css/*.css',
                'tagging_ext/*.css',
                'pinax/css/*.css',
                'uni_form/*.css',
                'frontendadmin/css/*.css',
                'filebrowser/css/*.css',
                'debug_toolbar/css/*.css',
                'bookmarks/css/*.css',
                'admin/css/*.css',
                'css/*.css',
                filters='cssmin', output='gen/all.css')

register('js_top', js_top)
register('js_bottom', js_bottom)
register('css_all', css_all)
