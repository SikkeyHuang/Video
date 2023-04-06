import socket
import cv2
import numpy as np

Host = ''
port = 8000

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((Host, port))
server_socket.listen(1)

# Initialize OpenCV window for displaying frames
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while True:
    # Wait for client to connect
    client_socket, addr = server_socket.accept()
    print('Client connected:', addr)

    while True:
        # Receive frame from client
        data = b''
        # a frame encoded with jpeg ends with '\xff\xd9'
        while b'\xff\xd9' not in data:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Close the client socket
    client_socket.close()

# Clean up
server_socket.close()
cv2.destroyAllWindows()

