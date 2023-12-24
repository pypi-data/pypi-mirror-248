import unittest
from PFDiscord.web_utils import (fetch_url, strip_html_markup, InvalidURLException, InsecureURLException)


class TestWebUtils(unittest.IsolatedAsyncioTestCase):

    async def test_invalid_url(self):
        with self.assertRaises(InvalidURLException):
            await fetch_url("not-a-valid-url")

    async def test_insecure_url(self):
        with self.assertRaises(InsecureURLException):
            await fetch_url("http://insecure.com")

    async def test_strip_html_markup(self):
        clean_content = strip_html_markup("<div>Hello</div>")
        self.assertEqual(clean_content, "Hello")


if __name__ == '__main__':
    unittest.main()
