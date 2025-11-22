from pymcprotocol_wrapper.client import Client
from pymcprotocol_wrapper.mock_client import MockClient
import unittest


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.mock_client = MockClient(require_connection=True)
        self.mock_client.connect()

    def test_connect(self):
        self.assertTrue(self.mock_client.connect())
        self.assertTrue(self.client.connect())

    def test_read_data(self):
        self.mock_client.write_data("D100", 123)
        data = self.mock_client.read_data("D100")
        self.assertEqual(data, 123)

        self.client.write_data("D100", 456)
        data = self.client.read_data("D100")
        self.assertEqual(data, 456)

    def test_write_data(self):
        self.mock_client.write_data("D200", 789)
        data = self.mock_client.read_data("D200")
        self.assertEqual(data, 789)

        self.client.write_data("D200", 101112)
        data = self.client.read_data("D200")
        self.assertEqual(data, 101112)

    def tearDown(self):
        self.client.disconnect()
        self.mock_client.disconnect()


if __name__ == '__main__':
    unittest.main()
