from requests import Session

from scrapping.instagram.constants.instagram_paths import INSTAGRAM_ORIGIN


DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


class InstagramSessionFactory:
    def __init__(self, config):
        self.config = config

    def create(self) -> Session:
        session = Session()

        session.headers.update(self._build_headers())
        session.cookies.update(self._build_cookies())

        return session

    def _build_headers(self):
        return {
            "User-Agent": DEFAULT_USER_AGENT,
            "X-CSRFToken": self.config.csrf_token,
            "Referer": INSTAGRAM_ORIGIN,
        }

    def _build_cookies(self):
        return {
            "sessionid": self.config.session_id,
            "csrftoken": self.config.csrf_token,
        }
