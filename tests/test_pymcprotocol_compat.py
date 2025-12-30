"""Tests for pymcprotocol-compatible API methods."""
from unittest import TestCase
from pymcprotocol_wrapper.client import Client
from pymcprotocol_wrapper.mock_client import MockClient


class TestPymcprotocolCompatAPI(TestCase):
    """Test pymcprotocol-compatible methods on both Client and MockClient."""

    def setUp(self):
        self.client = Client()
        self.client.connect()
        
        self.mock_client = MockClient(require_connection=True)
        self.mock_client.connect()

    def tearDown(self):
        self.client.close()
        self.mock_client.close()

    def test_close_method(self):
        """Test close() method as alias for disconnect()."""
        # Should work for both clients
        self.assertTrue(self.client.close())
        self.assertTrue(self.mock_client.close())
        
        self.assertFalse(self.client._connected)
        self.assertFalse(self.mock_client.connected)

    def test_setaccessopt(self):
        """Test setaccessopt() method."""
        # Should not raise errors
        self.client.setaccessopt(commtype="binary")
        self.mock_client.setaccessopt(commtype="ascii", network=1, pc=2)
        
        # Verify options are stored in client
        self.assertEqual(self.client._commtype, "binary")

    def test_batchread_wordunits(self):
        """Test batchread_wordunits() method."""
        # Write some test data first
        self.client.batchwrite_wordunits("D100", [10, 20, 30, 40, 50])
        self.mock_client.batchwrite_wordunits("D100", [10, 20, 30, 40, 50])
        
        # Read it back
        client_values = self.client.batchread_wordunits("D100", 5)
        mock_values = self.mock_client.batchread_wordunits("D100", 5)
        
        self.assertEqual(client_values, [10, 20, 30, 40, 50])
        self.assertEqual(mock_values, [10, 20, 30, 40, 50])

    def test_batchread_bitunits(self):
        """Test batchread_bitunits() method."""
        # Write some test data
        self.client.batchwrite_bitunits("X10", [1, 0, 1, 1, 0])
        self.mock_client.batchwrite_bitunits("X10", [1, 0, 1, 1, 0])
        
        # Read it back
        client_values = self.client.batchread_bitunits("X10", 5)
        mock_values = self.mock_client.batchread_bitunits("X10", 5)
        
        self.assertEqual(client_values, [1, 0, 1, 1, 0])
        self.assertEqual(mock_values, [1, 0, 1, 1, 0])

    def test_batchwrite_wordunits(self):
        """Test batchwrite_wordunits() method."""
        # Write values
        self.client.batchwrite_wordunits("D200", [100, 200, 300])
        self.mock_client.batchwrite_wordunits("D200", [100, 200, 300])
        
        # Verify by reading back
        self.assertEqual(self.client.read_data("D200"), 100)
        self.assertEqual(self.client.read_data("D201"), 200)
        self.assertEqual(self.client.read_data("D202"), 300)
        
        self.assertEqual(self.mock_client.read_data("D200"), 100)
        self.assertEqual(self.mock_client.read_data("D201"), 200)
        self.assertEqual(self.mock_client.read_data("D202"), 300)

    def test_batchwrite_bitunits(self):
        """Test batchwrite_bitunits() method."""
        # Write values
        self.client.batchwrite_bitunits("Y20", [1, 1, 0, 1])
        self.mock_client.batchwrite_bitunits("Y20", [1, 1, 0, 1])
        
        # Verify by reading back
        self.assertEqual(self.client.read_data("Y20"), 1)
        self.assertEqual(self.client.read_data("Y21"), 1)
        self.assertEqual(self.client.read_data("Y22"), 0)
        self.assertEqual(self.client.read_data("Y23"), 1)
        
        self.assertEqual(self.mock_client.read_data("Y20"), 1)
        self.assertEqual(self.mock_client.read_data("Y21"), 1)
        self.assertEqual(self.mock_client.read_data("Y22"), 0)
        self.assertEqual(self.mock_client.read_data("Y23"), 1)

    def test_randomread(self):
        """Test randomread() method."""
        # Write some test data
        self.client.write_data("D100", 111)
        self.client.write_data("D200", 222)
        self.client.write_data("D300", 333)
        
        self.mock_client.write_data("D100", 111)
        self.mock_client.write_data("D200", 222)
        self.mock_client.write_data("D300", 333)
        
        # Random read
        word_vals, dword_vals = self.client.randomread(
            word_devices=["D100", "D200"], 
            dword_devices=["D300"]
        )
        mock_word_vals, mock_dword_vals = self.mock_client.randomread(
            word_devices=["D100", "D200"], 
            dword_devices=["D300"]
        )
        
        self.assertEqual(word_vals, [111, 222])
        self.assertEqual(dword_vals, [333])
        self.assertEqual(mock_word_vals, [111, 222])
        self.assertEqual(mock_dword_vals, [333])

    def test_randomwrite(self):
        """Test randomwrite() method."""
        # Random write
        self.client.randomwrite(
            word_devices=["D400", "D500"], 
            word_values=[444, 555],
            dword_devices=["D600"],
            dword_values=[666]
        )
        self.mock_client.randomwrite(
            word_devices=["D400", "D500"], 
            word_values=[444, 555],
            dword_devices=["D600"],
            dword_values=[666]
        )
        
        # Verify
        self.assertEqual(self.client.read_data("D400"), 444)
        self.assertEqual(self.client.read_data("D500"), 555)
        self.assertEqual(self.client.read_data("D600"), 666)
        
        self.assertEqual(self.mock_client.read_data("D400"), 444)
        self.assertEqual(self.mock_client.read_data("D500"), 555)
        self.assertEqual(self.mock_client.read_data("D600"), 666)

    def test_randomwrite_bitunits(self):
        """Test randomwrite_bitunits() method."""
        # Random write bits
        self.client.randomwrite_bitunits(
            bit_devices=["X100", "X200", "X300"],
            values=[1, 0, 1]
        )
        self.mock_client.randomwrite_bitunits(
            bit_devices=["X100", "X200", "X300"],
            values=[1, 0, 1]
        )
        
        # Verify
        self.assertEqual(self.client.read_data("X100"), 1)
        self.assertEqual(self.client.read_data("X200"), 0)
        self.assertEqual(self.client.read_data("X300"), 1)
        
        self.assertEqual(self.mock_client.read_data("X100"), 1)
        self.assertEqual(self.mock_client.read_data("X200"), 0)
        self.assertEqual(self.mock_client.read_data("X300"), 1)

    def test_read_cputype(self):
        """Test read_cputype() method."""
        # Should return a CPU type string
        client_cpu = self.client.read_cputype()
        mock_cpu = self.mock_client.read_cputype()
        
        self.assertIsNotNone(client_cpu)
        self.assertEqual(mock_cpu, "Q03UDECPU")

    def test_echo_test(self):
        """Test echo_test() method."""
        # Test with data
        test_data = b"test123"
        client_echo = self.client.echo_test(test_data)
        mock_echo = self.mock_client.echo_test(test_data)
        
        self.assertEqual(client_echo, test_data)
        self.assertEqual(mock_echo, test_data)
        
        # Test without data
        client_echo = self.client.echo_test()
        mock_echo = self.mock_client.echo_test()
        
        self.assertIsNotNone(client_echo)
        self.assertIsNotNone(mock_echo)

    def test_remote_control_methods(self):
        """Test remote control methods (run, stop, pause, reset, etc.)."""
        # These should not raise errors
        self.client.remote_run()
        self.client.remote_stop()
        self.client.remote_pause()
        self.client.remote_reset()
        self.client.remote_latchclear()
        self.client.remote_unlock("1234")
        self.client.remote_lock("1234")
        
        self.mock_client.remote_run()
        self.mock_client.remote_stop()
        self.mock_client.remote_pause()
        self.mock_client.remote_reset()
        self.mock_client.remote_latchclear()
        self.mock_client.remote_unlock("1234")
        self.mock_client.remote_lock("1234")

    def test_connect_with_parameters(self):
        """Test connect() method with IP and port parameters."""
        client = Client()
        # Should accept IP and port in connect() call
        result = client.connect(ip="192.168.1.1", port=5000)
        self.assertTrue(result)
        self.assertEqual(client.ip_address, "192.168.1.1")
        self.assertEqual(client.port, 5000)
        client.close()

    def test_empty_randomread(self):
        """Test randomread() with empty device lists."""
        word_vals, dword_vals = self.client.randomread()
        self.assertEqual(word_vals, [])
        self.assertEqual(dword_vals, [])
        
        word_vals, dword_vals = self.mock_client.randomread()
        self.assertEqual(word_vals, [])
        self.assertEqual(dword_vals, [])

    def test_empty_randomwrite(self):
        """Test randomwrite() with empty device lists."""
        # Should not raise errors
        self.client.randomwrite()
        self.mock_client.randomwrite()


if __name__ == '__main__':
    import unittest
    unittest.main()
