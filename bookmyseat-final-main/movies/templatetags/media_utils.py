from django import template
from django.utils.safestring import mark_safe
import re
register=template.Library()
@register.filter(name='get_embed_source')
def get_trailer_src_url(original_link):
    if not original_link:
        return ""
    yt_regex_pattern=r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch/?v=))([\w-]{11})(?:[&\?].*]?$)"
    match_result=re.search(yt_regex_pattern, original_link)
    if match_result:
        final_video_id=match_result.group(1)
        secure_embed_path=f"https://www.youtube.com/embed/{final_video_id}"
        return mark_safe(secure_embed_path)
    return ""