DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}


def build_request_cookies(config):
    session_id = config["session_id"]
    return {"sessionid": session_id}


def build_request_headers(config):
    return config.get("headers", DEFAULT_REQUEST_HEADERS)
