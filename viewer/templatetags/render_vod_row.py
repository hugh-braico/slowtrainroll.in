from django import template
from django.utils.html import format_html

register = template.Library()

#Done this way so we can pass the "icon_dir" parameter into the vod function

@register.simple_tag
def render_vod_row(vod, icon_dir):
    return format_html(vod.table_row_html(icon_dir))