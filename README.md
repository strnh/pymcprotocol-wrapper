# pymcprotocol-wrapper

## Overview

The `pymcprotocol-wrapper` is a Python package that provides a convenient interface for interacting with PLCs using the `pymcprotocol` library. This wrapper implements the full `pymcprotocol` Type3E API, allowing developers to easily connect to PLCs, read and write data, and perform various operations. It includes a fallback mock mode for testing without a physical PLC connection.

## Features

- **Full pymcprotocol Type3E API Compatibility**: Implements all main methods from pymcprotocol's Type3E class for seamless integration
- **Client Class**: A robust implementation that wraps the `pymcprotocol` library for real PLC communication with automatic fallback to mock mode
- **Mock Client**: A simulated client for testing and development purposes, implementing the same API as the real client
- **Batch Operations**: Read and write consecutive word/bit units efficiently
- **Random Access**: Read and write non-consecutive device addresses
- **Remote Control**: Execute PLC control commands (RUN, STOP, PAUSE, RESET, etc.)
- **Backward Compatibility**: Simplified `read_data()` and `write_data()` methods still available
- **Utility Functions**: Helpful functions for data conversion and validation

## Installation

To install the `pymcprotocol-wrapper`, you can use pip:

```bash
pip install pymcprotocol-wrapper
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/pymcprotocol-wrapper.git
cd pymcprotocol-wrapper
pip install .
```

## Usage

### pymcprotocol-Compatible API (Recommended)

The wrapper now provides full compatibility with pymcprotocol's Type3E API:

```python
from pymcprotocol_wrapper import Client

# Create a client instance
client = Client(plctype="Q")

# Connect to the PLC
client.connect(ip="192.168.1.10", port=5000)

# Set communication options
client.setaccessopt(commtype="binary")

# Batch read/write word units
client.batchwrite_wordunits(headdevice="D100", values=[10, 20, 30, 40, 50])
values = client.batchread_wordunits(headdevice="D100", readsize=5)
print(values)  # [10, 20, 30, 40, 50]

# Batch read/write bit units
client.batchwrite_bitunits(headdevice="Y10", values=[1, 0, 1, 1, 0])
bits = client.batchread_bitunits(headdevice="Y10", readsize=5)
print(bits)  # [1, 0, 1, 1, 0]

# Random read/write (non-consecutive addresses)
client.randomwrite(
    word_devices=["D200", "D300", "D400"],
    word_values=[200, 300, 400]
)
word_vals, dword_vals = client.randomread(
    word_devices=["D200", "D300"]
)

# Get CPU type
cpu_type = client.read_cputype()

# Test communication
echo_response = client.echo_test(b"test")

# Remote control (use with caution!)
# client.remote_run()
# client.remote_stop()

# Close connection
client.close()
```

### Simplified API (Backward Compatible)

The original simplified API is still available for backward compatibility:

```python
from pymcprotocol_wrapper import Client

# Create a client instance
client = Client()
client.connect()

# Read/write single addresses
client.write_data('D100', 123)
data = client.read_data('D100')

# Disconnect
client.disconnect()
```

### Mock Client for Testing

Use MockClient for testing without a real PLC:

```python
from pymcprotocol_wrapper import MockClient

# Create a mock client
mock_client = MockClient(require_connection=True)
mock_client.connect()

# All pymcprotocol API methods work the same
mock_client.batchwrite_wordunits("D100", [1, 2, 3])
values = mock_client.batchread_wordunits("D100", 3)

mock_client.close()
```

For more detailed usage examples, please refer to the `examples/` directory:
- `examples/simple_usage.py` - Basic backward-compatible usage
- `examples/pymcprotocol_compatible_usage.py` - Full pymcprotocol API examples

## API Reference

### Connection Methods
- `connect(ip=None, port=None)` - Connect to PLC
- `close()` / `disconnect()` - Disconnect from PLC
- `setaccessopt(commtype, network, pc, dest_moduleio, dest_modulesta)` - Set communication options

### Batch Operations
- `batchread_wordunits(headdevice, readsize)` - Read consecutive word registers
- `batchread_bitunits(headdevice, readsize)` - Read consecutive bits
- `batchwrite_wordunits(headdevice, values)` - Write consecutive word registers
- `batchwrite_bitunits(headdevice, values)` - Write consecutive bits

### Random Access
- `randomread(word_devices, dword_devices)` - Read non-consecutive devices
- `randomwrite(word_devices, word_values, dword_devices, dword_values)` - Write non-consecutive devices
- `randomwrite_bitunits(bit_devices, values)` - Write non-consecutive bits

### System Operations
- `read_cputype()` - Read PLC CPU type
- `echo_test(echo_data)` - Test communication

### Remote Control
- `remote_run(clear_mode, force_exec)` - Start PLC
- `remote_stop()` - Stop PLC
- `remote_pause(latch)` - Pause PLC
- `remote_reset()` - Reset PLC
- `remote_latchclear()` - Clear latch
- `remote_unlock(password)` - Unlock PLC
- `remote_lock(password)` - Lock PLC

### Legacy Methods (Backward Compatible)
- `read_data(address)` - Read single address
- `write_data(address, value)` - Write single address

## Testing

To run the tests for the `pymcprotocol-wrapper`, you can use:

```bash
pytest tests/
```

Make sure to have the development dependencies installed as specified in `requirements-dev.txt`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
