import unittest

from intelligence_hub.src.text import clean_text


class TextTest(unittest.TestCase):
    def test_clean_text_unescapes_html_entities(self):
        value = "AI&nbsp;agent &#160; update &#8230; &amp; workflow <b>demo</b>"
        self.assertEqual(clean_text(value), "AI agent update … & workflow demo")


if __name__ == "__main__":
    unittest.main()
