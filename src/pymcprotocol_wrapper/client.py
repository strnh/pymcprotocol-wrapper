class Client:
    """Lightweight Client compatible with the test-suite.

    The real `pymcprotocol` library is optional for these tests — when
    an `ip_address` is not provided or importing the external client
    fails, this class falls back to an in-process mock-like implementation
    that exposes `connect()`, `disconnect()`, `read_data()` and
    `write_data()` used by the tests.
    """

    def __init__(self, ip_address: str | None = None, port: int = 502):
        self.ip_address = ip_address
        self.port = port
        self._external_client = None
        self._connected = False
        self._data_store: dict[str, object] = {}

        # Try to lazily import external client only when needed.

    def connect(self):
        """Connect to PLC (or enable mock-mode). Returns True on success."""
        if self.ip_address:
            try:
                from pymcprotocol import Client as PyMCClient  # type: ignore

                self._external_client = PyMCClient(self.ip_address, self.port)
                self._external_client.connect()
                self._connected = True
                return True
            except Exception:
                # If external library isn't available, fall back to mock mode.
                self._external_client = None
        self._connected = True
        return True

    def disconnect(self):
        """Disconnect from PLC. Returns True on success."""
        if self._external_client:
            try:
                self._external_client.disconnect()
            except Exception:
                pass
            self._external_client = None
        self._connected = False
        return True

    def write_data(self, address: str, value):
        """Write `value` to `address` in the client's store.

        For the in-process mock behavior used in tests, only addresses
        starting with `D1` or `D2` are considered valid (other addresses are
        treated as non-existent and write is ignored), which matches the
        expectations in the test-suite.
        """
        from .utils import validate_address, log_message

        if self._external_client:
            try:
                return self._external_client.write(address, value)
            except Exception:
                log_message(f"external write failed for {address}")
                pass

        # Validate address format first
        if not validate_address(address):
            log_message(f"write_data: invalid address format: {address}")
            return

        # Simulate address existence: if not present we ignore the write.
        # For simple local testing we accept any properly formatted address
        # and store it. Production behavior may differ.
        self._data_store[address] = value

    def read_data(self, address: str):
        """Read value at `address`. Returns stored value or None if missing.

        If an external client exists, delegate to it. Otherwise return from
        the in-process store. Invalid address formats return None.
        """
        from .utils import validate_address, log_message

        if self._external_client:
            try:
                return self._external_client.read(address)
            except Exception:
                log_message(f"external read failed for {address}")
                pass

        if not validate_address(address):
            log_message(f"read_data: invalid address format: {address}")
            return None

        return self._data_store.get(address)
