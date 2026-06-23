from urllib.parse import urlencode

import requests

from scrapping.instagram.instagram_constants import INSTAGRAM_MEDIA_COMMENTS_PATH
from scrapping.instagram.instagram_support import build_request_cookies, build_request_headers
from scrapping.scraping_utils import bool_to_str, sleep_random


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


def fetch_comments_page(config):
    media_id = config["media_id"]
    can_support_threading = config.get("can_support_threading", False)
    permalink_enabled = config.get("permalink_enabled", False)
    min_id = config.get("min_id")

    url = get_scrap_comments_url(
        media_id,
        can_support_threading=can_support_threading,
        permalink_enabled=permalink_enabled,
        min_id=min_id,
    )

    response = requests.get(
        url,
        cookies=build_request_cookies(config),
        headers=build_request_headers(config),
    )
    response.raise_for_status()

    return response.json()


def fetch_all_comment_pages(config):
    pages = []
    min_id = None

    while True:
        comments_page_config = {**config, "min_id": min_id}
        payload = fetch_comments_page(comments_page_config)
        pages.append(payload)

        if not payload.get("next_min_id"):
            break

        sleep_random()
        min_id = payload["next_min_id"]

    return pages
