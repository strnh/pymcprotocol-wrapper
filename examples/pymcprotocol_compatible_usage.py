"""Example demonstrating pymcprotocol-compatible API usage.

This example shows how to use the pymcprotocol-wrapper with the
same API as the original pymcprotocol library's Type3E class.
"""

from pymcprotocol_wrapper import Client, MockClient


def example_with_real_plc():
    """Example using Client with a real PLC (or mock mode if no IP provided)."""
    print("=" * 60)
    print("Example 1: Using Client (pymcprotocol compatible API)")
    print("=" * 60)
    
    # Create client instance (similar to pymcprotocol.Type3E)
    client = Client(plctype="Q")
    
    # Option 1: Connect without IP (falls back to mock mode)
    client.connect()
    
    # Option 2: Connect with IP and port (would connect to real PLC)
    # client.connect(ip="192.168.1.10", port=5000)
    
    # Set communication options (pymcprotocol compatible)
    client.setaccessopt(commtype="binary")
    
    print("\n--- Batch Write/Read Operations ---")
    # Batch write word units (consecutive addresses)
    client.batchwrite_wordunits(headdevice="D100", values=[10, 20, 30, 40, 50])
    print("Wrote values [10, 20, 30, 40, 50] to D100-D104")
    
    # Batch read word units
    values = client.batchread_wordunits(headdevice="D100", readsize=5)
    print(f"Read values from D100-D104: {values}")
    
    print("\n--- Bit Operations ---")
    # Batch write bit units
    client.batchwrite_bitunits(headdevice="Y10", values=[1, 0, 1, 1, 0])
    print("Wrote bits [1, 0, 1, 1, 0] to Y10-Y14")
    
    # Batch read bit units
    bits = client.batchread_bitunits(headdevice="Y10", readsize=5)
    print(f"Read bits from Y10-Y14: {bits}")
    
    print("\n--- Random Access Operations ---")
    # Random write (non-consecutive addresses)
    client.randomwrite(
        word_devices=["D200", "D300", "D400"],
        word_values=[200, 300, 400],
        dword_devices=["D500"],
        dword_values=[500]
    )
    print("Random write to D200, D300, D400, D500")
    
    # Random read (non-consecutive addresses)
    word_vals, dword_vals = client.randomread(
        word_devices=["D200", "D300"],
        dword_devices=["D500"]
    )
    print(f"Random read word values: {word_vals}")
    print(f"Random read dword values: {dword_vals}")
    
    # Random write bit units
    client.randomwrite_bitunits(
        bit_devices=["X100", "X200", "X300"],
        values=[1, 0, 1]
    )
    print("Random write bits to X100, X200, X300")
    
    print("\n--- System Operations ---")
    # Get CPU type
    cpu_type = client.read_cputype()
    print(f"PLC CPU Type: {cpu_type}")
    
    # Echo test
    echo_response = client.echo_test(b"test123")
    print(f"Echo test response: {echo_response}")
    
    print("\n--- Remote Control Operations ---")
    # Note: These are for demonstration only - use with caution on real PLCs!
    # client.remote_run(clear_mode=0)  # Start PLC
    # client.remote_stop()              # Stop PLC
    # client.remote_pause()             # Pause PLC
    # client.remote_reset()             # Reset PLC
    # client.remote_unlock("password")  # Unlock PLC
    # client.remote_lock("password")    # Lock PLC
    print("Remote control methods available (commented out for safety)")
    
    # Close connection (pymcprotocol compatible - alias for disconnect)
    client.close()
    print("\nConnection closed")


def example_with_mock_client():
    """Example using MockClient for testing."""
    print("\n" + "=" * 60)
    print("Example 2: Using MockClient (for testing)")
    print("=" * 60)
    
    # Create mock client
    mock = MockClient(require_connection=True)
    mock.connect()
    
    print("\n--- Testing with MockClient ---")
    # All the same methods work with MockClient
    mock.batchwrite_wordunits("D100", [11, 22, 33])
    values = mock.batchread_wordunits("D100", 3)
    print(f"MockClient batch read: {values}")
    
    # Random operations
    mock.randomwrite(word_devices=["D200", "D300"], word_values=[200, 300])
    word_vals, _ = mock.randomread(word_devices=["D200", "D300"])
    print(f"MockClient random read: {word_vals}")
    
    # System info
    cpu = mock.read_cputype()
    print(f"MockClient CPU type: {cpu}")
    
    mock.close()
    print("MockClient closed")


def example_backward_compatibility():
    """Example showing backward compatibility with simplified API."""
    print("\n" + "=" * 60)
    print("Example 3: Backward Compatibility (simplified API)")
    print("=" * 60)
    
    # The old simplified API still works
    client = Client()
    client.connect()
    
    # Old methods still available
    client.write_data("D100", 123)
    value = client.read_data("D100")
    print(f"Using old API - read_data('D100'): {value}")
    
    client.disconnect()  # Old method
    print("Old API methods still work for backward compatibility")


if __name__ == "__main__":
    # Run all examples
    example_with_real_plc()
    example_with_mock_client()
    example_backward_compatibility()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
