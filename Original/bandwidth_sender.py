import socket
import time

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Initialize data to send
data = b'\x00' * 1024  # 1 KB of data

# Continuously send data to server
while True:
    start_time = time.monotonic()
    client_socket.sendall(data)
    response = client_socket.recv(1024)
    elapsed_time = time.monotonic() - start_time

    # Print the round-trip time and calculated bandwidth
    rtt = elapsed_time * 1000  # Round-trip time in milliseconds
    bandwidth = len(data) / elapsed_time / 1000 / 1000  # Bandwidth in Mbps
    print(f'RTT: {rtt:.2f} ms    Bandwidth: {bandwidth:.2f} Mbps')

# Clean up
client_socket.close()
