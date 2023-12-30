from unittest import TestCase
import requests

from onionrequests.OnionQueue import OnionQueue
from onionrequests.OnionSession import OnionSession

CONST_TEST_IP_URL = "https://www.httpbin.org/ip"


class TestOnionSession(TestCase):
    def test_anonymous_ipv4_address(self):
        with requests.get(CONST_TEST_IP_URL, timeout=5) as res:
            res.raise_for_status()
            current_ip = res.json()["origin"]
            self.assertIsInstance(current_ip, str)
            self.assertTrue(len(current_ip) >= len("0.0.0.0"))

        with OnionSession().get(CONST_TEST_IP_URL, timeout=5) as res:
            res.raise_for_status()
            anonymous_ip = res.json()["origin"]
            self.assertIsInstance(anonymous_ip, str)
            self.assertTrue(len(anonymous_ip) >= len("0.0.0.0"))

        self.assertNotEqual(current_ip, anonymous_ip)

    def test_consistent_ipv4_address(self):
        session = OnionSession()

        with session.get(CONST_TEST_IP_URL, timeout=5) as res:
            res.raise_for_status()
            old_ip = res.json()["origin"]
            self.assertIsInstance(old_ip, str)
            self.assertTrue(len(old_ip) >= len("0.0.0.0"))

        with session.get(CONST_TEST_IP_URL, timeout=5) as res:
            res.raise_for_status()
            new_ip = res.json()["origin"]
            self.assertIsInstance(new_ip, str)
            self.assertTrue(len(new_ip) >= len("0.0.0.0"))

        self.assertEqual(old_ip, new_ip)


class TestOnionQueue(TestCase):
    def test_anonymous_ipv4_address(self):
        duplicate_error = 2  # Some TOR sessions use the same public IPv4 address. Allow error for a few duplicates.

        with requests.get(CONST_TEST_IP_URL, timeout=5) as res:
            res.raise_for_status()
            current_ip = res.json()["origin"]
            self.assertIsInstance(current_ip, str)
            self.assertTrue(len(current_ip) >= len("0.0.0.0"))

        queue = OnionQueue(num_threads=10)
        queue.start()

        anonymous_ips = []
        for session in queue.sessions:
            with session.get(CONST_TEST_IP_URL, timeout=5) as res:
                res.raise_for_status()
                anonymous_ip = res.json()["origin"]
                self.assertIsInstance(anonymous_ip, str)
                self.assertTrue(len(anonymous_ip) >= len("0.0.0.0"))
                self.assertNotEqual(current_ip, anonymous_ip)
                anonymous_ips.append(anonymous_ip)
                self.assertTrue(anonymous_ips.count(anonymous_ip) <= duplicate_error)

    def test_consistent_ipv4_address(self):
        queue = OnionQueue(num_threads=5)
        queue.start()

        for session in queue.sessions:
            with session.get(CONST_TEST_IP_URL, timeout=5) as res:
                res.raise_for_status()
                old_ip = res.json()["origin"]
                self.assertIsInstance(old_ip, str)
                self.assertTrue(len(old_ip) >= len("0.0.0.0"))

            with session.get(CONST_TEST_IP_URL, timeout=5) as res:
                res.raise_for_status()
                new_ip = res.json()["origin"]
                self.assertIsInstance(new_ip, str)
                self.assertTrue(len(new_ip) >= len("0.0.0.0"))

            self.assertEqual(old_ip, new_ip)


