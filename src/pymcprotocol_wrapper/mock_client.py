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

    def close(self):
        """Close connection (pymcprotocol compatible alias for disconnect())."""
        return self.disconnect()

    def setaccessopt(self, commtype: str | None = None, network: int | None = None,
                     pc: int | None = None, dest_moduleio: int | None = None,
                     dest_modulesta: int | None = None):
        """Set communication options (pymcprotocol compatible method).
        
        Mock implementation - stores but doesn't use these options.
        """
        # Mock implementation - just store the values but don't use them
        pass

    def batchread_wordunits(self, headdevice: str, readsize: int):
        """Read consecutive word units (pymcprotocol compatible method).
        
        Args:
            headdevice: Starting device address (e.g., "D100")
            readsize: Number of words to read
            
        Returns:
            List of integer values
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if not validate_address(headdevice):
            log_message(f"MockClient.batchread_wordunits: invalid address format: {headdevice}")
            return []
        
        device_type = headdevice[0]
        try:
            start_num = int(headdevice[1:])
        except ValueError:
            return []
        
        result = []
        for i in range(readsize):
            addr = f"{device_type}{start_num + i}"
            value = self.data_store.get(addr, 0)
            result.append(value)
        return result

    def batchread_bitunits(self, headdevice: str, readsize: int):
        """Read consecutive bit units (pymcprotocol compatible method).
        
        Args:
            headdevice: Starting device address (e.g., "X10")
            readsize: Number of bits to read
            
        Returns:
            List of 0/1 values
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if not validate_address(headdevice):
            log_message(f"MockClient.batchread_bitunits: invalid address format: {headdevice}")
            return []
        
        device_type = headdevice[0]
        try:
            start_num = int(headdevice[1:])
        except ValueError:
            return []
        
        result = []
        for i in range(readsize):
            addr = f"{device_type}{start_num + i}"
            value = self.data_store.get(addr, 0)
            result.append(1 if value else 0)
        return result

    def batchwrite_wordunits(self, headdevice: str, values: list):
        """Write consecutive word units (pymcprotocol compatible method).
        
        Args:
            headdevice: Starting device address (e.g., "D100")
            values: List of integer values to write
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if not validate_address(headdevice):
            log_message(f"MockClient.batchwrite_wordunits: invalid address format: {headdevice}")
            return
        
        device_type = headdevice[0]
        try:
            start_num = int(headdevice[1:])
        except ValueError:
            return
        
        for i, value in enumerate(values):
            addr = f"{device_type}{start_num + i}"
            num = start_num + i
            if 0 <= num <= 0xFFFFFF:
                self.data_store[addr] = value

    def batchwrite_bitunits(self, headdevice: str, values: list):
        """Write consecutive bit units (pymcprotocol compatible method).
        
        Args:
            headdevice: Starting device address (e.g., "Y10")
            values: List of 0/1 values to write
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if not validate_address(headdevice):
            log_message(f"MockClient.batchwrite_bitunits: invalid address format: {headdevice}")
            return
        
        device_type = headdevice[0]
        try:
            start_num = int(headdevice[1:])
        except ValueError:
            return
        
        for i, value in enumerate(values):
            addr = f"{device_type}{start_num + i}"
            num = start_num + i
            if 0 <= num <= 0xFFFFFF:
                self.data_store[addr] = 1 if value else 0

    def randomread(self, word_devices: list | None = None, dword_devices: list | None = None):
        """Read non-consecutive devices (pymcprotocol compatible method).
        
        Args:
            word_devices: List of word device addresses
            dword_devices: List of double-word device addresses
            
        Returns:
            Tuple of (word_values, dword_values)
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if word_devices is None:
            word_devices = []
        if dword_devices is None:
            dword_devices = []
        
        word_values = []
        for addr in word_devices:
            if validate_address(addr):
                value = self.data_store.get(addr, 0)
                word_values.append(value)
            else:
                word_values.append(0)
        
        dword_values = []
        for addr in dword_devices:
            if validate_address(addr):
                value = self.data_store.get(addr, 0)
                dword_values.append(value)
            else:
                dword_values.append(0)
        
        return (word_values, dword_values)

    def randomwrite(self, word_devices: list | None = None, word_values: list | None = None,
                    dword_devices: list | None = None, dword_values: list | None = None):
        """Write non-consecutive devices (pymcprotocol compatible method).
        
        Args:
            word_devices: List of word device addresses
            word_values: List of values for word devices
            dword_devices: List of double-word device addresses
            dword_values: List of values for double-word devices
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        if word_devices is None:
            word_devices = []
        if word_values is None:
            word_values = []
        if dword_devices is None:
            dword_devices = []
        if dword_values is None:
            dword_values = []
        
        for addr, value in zip(word_devices, word_values):
            if validate_address(addr):
                try:
                    num = int(addr[1:])
                    if 0 <= num <= 0xFFFFFF:
                        self.data_store[addr] = value
                except ValueError:
                    pass
        
        for addr, value in zip(dword_devices, dword_values):
            if validate_address(addr):
                try:
                    num = int(addr[1:])
                    if 0 <= num <= 0xFFFFFF:
                        self.data_store[addr] = value
                except ValueError:
                    pass

    def randomwrite_bitunits(self, bit_devices: list, values: list):
        """Write non-consecutive bit devices (pymcprotocol compatible method).
        
        Args:
            bit_devices: List of bit device addresses
            values: List of 0/1 values
        """
        from .utils import validate_address, log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        for addr, value in zip(bit_devices, values):
            if validate_address(addr):
                try:
                    num = int(addr[1:])
                    if 0 <= num <= 0xFFFFFF:
                        self.data_store[addr] = 1 if value else 0
                except ValueError:
                    pass

    def read_cputype(self):
        """Read PLC CPU type (pymcprotocol compatible method).
        
        Returns:
            CPU type string
        """
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        return "Q03UDECPU"

    def echo_test(self, echo_data: bytes | None = None):
        """Test communication (pymcprotocol compatible method).
        
        Args:
            echo_data: Data to echo
            
        Returns:
            Echo response
        """
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        return echo_data if echo_data else b"OK"

    def remote_run(self, clear_mode: int = 0, force_exec: bool = False):
        """Execute remote RUN command (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message(f"MockClient.remote_run: clear_mode={clear_mode}, force_exec={force_exec}")

    def remote_stop(self):
        """Execute remote STOP command (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message("MockClient.remote_stop")

    def remote_pause(self, latch: bool = False):
        """Execute remote PAUSE command (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message(f"MockClient.remote_pause: latch={latch}")

    def remote_reset(self):
        """Execute remote RESET command (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message("MockClient.remote_reset")

    def remote_latchclear(self):
        """Execute remote LATCH CLEAR command (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message("MockClient.remote_latchclear")

    def remote_unlock(self, password: str = ""):
        """Unlock PLC (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message("MockClient.remote_unlock")

    def remote_lock(self, password: str = ""):
        """Lock PLC (pymcprotocol compatible method)."""
        from .utils import log_message
        
        if self.require_connection and not self.connected:
            raise ConnectionError("Not connected to the mock PLC.")
        
        log_message("MockClient.remote_lock")
