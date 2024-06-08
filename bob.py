import socket
import threading
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.connection_addresses = set()

    def connect(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            connection_address = (peer_host, peer_port)
            if connection_address not in self.connection_addresses:
                self.connections.append(connection)
                self.connection_addresses.add(connection_address)
                print(f"Connected to {peer_host}:{peer_port}")
                threading.Thread(target=self.handle_client, args=(connection, connection_address)).start()
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            if address not in self.connection_addresses:
                self.connections.append(connection)
                self.connection_addresses.add(address)
                print(f"Accepted connection from {address}")
                threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)
                self.connection_addresses.remove(connection.getpeername())

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received data from {address}: {data.decode()}")
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        self.connection_addresses.remove(address)
        connection.close()

    def start_listening(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

# Example usage:
if __name__ == "__main__":
    # Create a peer instance and start listening for incoming connections
    node = Peer("0.0.0.0", 8000)
    node.start_listening()

    # Give some time for the node to start listening
    time.sleep(2)

    # Connect to another peer (example IP address and port, change these accordingly)
    peer_host = input("Enter the peer IP address to connect to: ")
    peer_port = int(input("Enter the peer port to connect to: "))
    node.connect(peer_host, peer_port)

    # Send messages to connected peers
    while True:
        message = input("Enter message to send: ")
        node.send_data(message)
