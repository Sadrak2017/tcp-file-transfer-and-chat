class ConnectedClient:

    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address

    def get_client_socket(self):
        return self.client_socket

    def get_client_address(self):
        return self.client_address
