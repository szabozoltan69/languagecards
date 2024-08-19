from django.test import TestCase
from http import HTTPStatus

# Thanks to https://adamj.eu/tech/2020/02/10/robots-txt


class RobotsTxtTests(TestCase):

    def test_get(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "text/plain"
        assert response.content.startswith(b"User-agent: *\n")

    def test_post_disallowed(self):
        response = self.client.post("/robots.txt")

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
