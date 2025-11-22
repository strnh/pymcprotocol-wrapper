class MockClient:
    def __init__(self, require_connection: bool = False):
        """Test mock for PLC client.

        Args:
            require_connection: If True, `read_data`/`write_data` require
                `connect()` to have been called, otherwise a
                `ConnectionError` is raised. Default False for backward compatibility.
        """
        self.connected = False
        self.require_connection = require_connection
        self.data_store: dict[str, object] = {}

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False
        return True

    def is_connected(self):
        return self.connected

    def write_data(self, address: str, value):
        """Write to an address.

        Behavior:
        - If `address` format is invalid -> ignore and log.
        - If address is valid but outside simulated address space -> ignore (non-existent).
        - Otherwise store the value in the internal store.
        """
        from .utils import validate_address, log_message

        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")

        if not validate_address(address):
            log_message(f"MockClient.write_data: invalid address format: {address}")
            return

        # Simulate address existence using 24-bit address space (0..16777215).
        try:
            num = int(address[1:])
        except Exception:
            log_message(f"MockClient.write_data: could not parse numeric portion: {address}")
            return

        if num < 0 or num > 0xFFFFFF:
            # out of 24-bit range -> ignore
            log_message(f"MockClient.write_data: address out of range: {address}")
            return

        # Accept and store for any valid 24-bit address.
        self.data_store[address] = value

    def read_data(self, address: str):
        """Return stored value or None if the address does not exist.

        Invalid formats return None. Addresses outside the simulated address
        space return None as well.
        """
        from .utils import validate_address, log_message

        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")

        if not validate_address(address):
            log_message(f"MockClient.read_data: invalid address format: {address}")
            return None

        try:
            num = int(address[1:])
        except Exception:
            log_message(f"MockClient.read_data: could not parse numeric portion: {address}")
            return None

        if num < 0 or num > 0xFFFFFF:
            log_message(f"MockClient.read_data: address out of range: {address}")
            return None

        return self.data_store.get(address)

    def clear_data(self):
        self.data_store.clear()
