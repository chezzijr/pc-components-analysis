import unittest
from scraper.web import match_name

class TestMatchName(unittest.TestCase):
    def test_match_name(self):
        self.assertTrue(match_name("Bo mạch chủ ASUS PRIME B550M-A (WI-FI) II", "Asus PRIME B550M-A WIFI II"))

if __name__ == "__main__":
    unittest.main()
