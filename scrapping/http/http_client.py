from requests import Session


class HttpClient:
    def __init__(self, session: Session):
        self.session = session

    def get(self, url):
        response = self.session.get(url)
        response.raise_for_status()

        return response.json()
