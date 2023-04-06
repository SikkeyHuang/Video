import socket
import cv2
import numpy as np
from threading import Thread
import queue
import time

Host = ''
port = 9000

# Initialize socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((Host, port))
server_socket.listen(1)

# Accept client connection
client_socket, _ = server_socket.accept()

# Initialize queue for storing frames
max_queue_size = 10  # Maximum number of frames to buffer
frame_queue = queue.Queue(max_queue_size)

# Function to continuously receive frames from the client and add them to the queue
def receive_frames():
    while True:
        # Receive frame from client
        data = b''
        while b'\xff\xd9' not in data:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Add the frame to the queue
        if not frame_queue.full():
            frame_queue.put(frame)

# Start thread for receiving frames from the client
receive_thread = Thread(target=receive_frames)
receive_thread.start()

# Initialize OpenCV window for displaying frames and stats
cv2.namedWindow('Server', cv2.WINDOW_NORMAL)

frame_counter = 0  # Counter for keeping track of the number of frames processed
start_time = time.time()  # Time when processing started

while True:
    if not frame_queue.empty():
        # Get the frame from the queue and display it
        frame = frame_queue.get()

        # Update stats window
        fps = frame_counter / (time.time() - start_time)  # Calculate frame rate
        queue_size = frame_queue.qsize()  # Get number of frames in queue
        #stats_text = f'FPS: {fps:.2f}   Queue size: {queue_size}'
        stats_text = f'FPS: {fps:.2f} '
        cv2.putText(frame, stats_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow('Server', frame)

        frame_counter += 1

    if cv2.waitKey(1) == ord('q'):
        break


# Clean up
receive_thread.join()
server_socket.close()
cv2.destroyAllWindows()
