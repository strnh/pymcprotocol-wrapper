# pymcprotocol-wrapper

## Overview

The `pymcprotocol-wrapper` is a Python package that provides a convenient interface for interacting with PLCs using the `pymcprotocol` library. This wrapper allows developers to easily connect to PLCs, read and write data, and perform various operations without needing to directly interact with the underlying protocol.

## Features

- **Client Class**: A robust implementation that wraps the `pymcprotocol` library for seamless PLC communication.
- **Mock Client**: A simulated client for testing and development purposes, allowing you to work without a physical PLC connection.
- **Utility Functions**: Helpful functions for data conversion and validation to support the main functionality of the wrapper.

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

### Basic Example

Here’s a simple example of how to use the `pymcprotocol-wrapper`:

```python
from pymcprotocol_wrapper.client import Client

# Create a client instance
client = Client()

# Connect to the PLC
client.connect()

# Read data from the PLC
data = client.read_data('D100')

# Write data to the PLC
client.write_data('D100', 123)

# Disconnect from the PLC
client.disconnect()
```

For more detailed usage, please refer to the examples provided in the `examples` directory.

## Testing

To run the tests for the `pymcprotocol-wrapper`, you can use:

```bash
pytest tests/
```

Make sure to have the development dependencies installed as specified in `requirements-dev.txt`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.