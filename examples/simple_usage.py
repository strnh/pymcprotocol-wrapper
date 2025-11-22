from pymcprotocol_wrapper.client import Client
from pymcprotocol_wrapper.mock_client import MockClient

def main():
    # Example usage of the Client class
    client = Client()
    client.connect('192.168.0.1', 502)  # Replace with actual PLC IP and port

    try:
        # Reading data from the PLC
        data = client.read_data('D1000')
        print(f'Read data from PLC: {data}')

        # Writing data to the PLC
        client.write_data('D1000', 123)
        print('Wrote data to PLC: 123')
    finally:
        client.disconnect()

    # Example usage of the MockClient class
    mock_client = MockClient()
    mock_client.connect()

    try:
        # Simulating reading data
        mock_data = mock_client.read_data('D1000')
        print(f'Read data from MockClient: {mock_data}')

        # Simulating writing data
        mock_client.write_data('D1000', 456)
        print('Wrote data to MockClient: 456')
    finally:
        mock_client.disconnect()

if __name__ == '__main__':
    main()