from django.utils.html import format_html_join
from django.conf import settings
from wagtail.core import hooks


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'countries/js/slug_from_country.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes