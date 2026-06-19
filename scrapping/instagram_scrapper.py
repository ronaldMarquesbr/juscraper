from urllib.parse import urlencode

from scrapping.instagram_constants import INSTAGRAM_MEDIA_COMMENTS_PATH
from scrapping.utils import bool_to_str


def get_scrap_comments_url(
    media_id,
    can_support_threading=False,
    permalink_enabled=False,
    min_id=None,
):
    base_url = INSTAGRAM_MEDIA_COMMENTS_PATH.format(media_id=media_id)

    params = {
        "can_support_threading": bool_to_str(can_support_threading),
        "permalink_enabled": bool_to_str(permalink_enabled),
    }
    
    if min_id is not None:
        params["min_id"] = min_id

    query_params = urlencode(params)

    return f"{base_url}?{query_params}"
