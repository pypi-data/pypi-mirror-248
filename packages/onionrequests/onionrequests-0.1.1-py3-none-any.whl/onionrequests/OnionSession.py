import random
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class OnionSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate a unique username and password to connect to TOR.
        random.seed(time.time_ns())
        username = str(time.time_ns()) + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))
        password = str(time.time_ns()) + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))

        # Tell the session to use HTTP through a TOR proxy.
        retry = Retry(connect=10, backoff_factor=1.0)
        adapter = HTTPAdapter(max_retries=retry)
        self.mount('http://', adapter)
        self.mount('https://', adapter)
        self.proxies = {
            'http': 'socks5://{}:{}@localhost:9050'.format(username, password),
            'https': 'socks5://{}:{}@localhost:9050'.format(username, password)
        }
