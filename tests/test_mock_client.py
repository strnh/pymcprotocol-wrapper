from unittest import TestCase
from pymcprotocol_wrapper.mock_client import MockClient


class TestMockClient(TestCase):

    def setUp(self):
        # Require explicit connect() for realistic behavior
        self.client = MockClient(require_connection=True)
        self.client.connect()

    def test_read_data(self):
        # Test reading data from the mock client
        address = "D1000"
        expected_value = 123  # Example expected value
        self.client.write_data(address, expected_value)
        value = self.client.read_data(address)
        self.assertEqual(value, expected_value)

    def test_write_data(self):
        # Test writing data to the mock client
        address = "D1001"
        value_to_write = 456
        self.client.write_data(address, value_to_write)
        value = self.client.read_data(address)
        self.assertEqual(value, value_to_write)

    def test_read_non_existent_address(self):
        # Test reading from a non-existent address
        address = "D9999"
        value = self.client.read_data(address)
        self.assertIsNone(value)

    def test_write_non_existent_address(self):
        # Test writing to a non-existent address
        address = "D9999"
        value_to_write = 789
        self.client.write_data(address, value_to_write)
        value = self.client.read_data(address)
        # With 16-bit address space, D9999 is a valid address and should store the value
        self.assertEqual(value, value_to_write)

    def test_multiple_writes_and_reads(self):
        # Test multiple writes and reads
        address = "D1002"
        for i in range(10):
            self.client.write_data(address, i)
            value = self.client.read_data(address)
            self.assertEqual(value, i)
