import socket
import time
# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen()

# Accept incoming connection
client_socket, address = server_socket.accept()

# Initialize variables for measuring bandwidth
total_bytes_received = 0
start_time = None

# Continuously receive data from client
while True:
    data = client_socket.recv(1024)
    if not data:
        break

    # Measure the time taken to receive data
    if start_time is None:
        start_time = time.monotonic()
    total_bytes_received += len(data)

    # Send a response to the client
    response = b'ACK'
    client_socket.sendall(response)

    # Calculate and print the current network bandwidth
    elapsed_time = time.monotonic() - start_time
    if elapsed_time >= 1.0:  # Only print every 1 second
        bandwidth = total_bytes_received / elapsed_time / 1000 / 1000
        print(f'Current bandwidth: {bandwidth:.2f} Mbps')

        # Reset variables for measuring bandwidth
        total_bytes_received = 0
        start_time = None

# Clean up
client_socket.close()
server_socket.close()
