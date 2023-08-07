from Common.http_client import HttpClient

class TestWorkSpace:
    def setup(self):
        self.hc = HttpClient()

    def teardown(self):
        self.hc.get_case_result()

