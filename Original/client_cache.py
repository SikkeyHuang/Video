import socket
import cv2
import numpy as np
from threading import Thread
import queue
import time

Host = ''
port = 9000

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#make the address and port reuseable
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

client_socket.connect((Host, port))

# Initialize queue for storing frames
max_queue_size = 10  # Maximum number of frames to buffer
frame_queue = queue.Queue(max_queue_size)

# Function to continuously capture frames from the camera and add them to the queue
def capture_frames():
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame from camera
        ret, frame = camera.read()
        if not ret:
            break

        # Add the frame to the queue
        if not frame_queue.full():
            frame_queue.put(frame)

    camera.release()

# Function to continuously send frames from the queue to the server
def send_frames():
    while True:
        # Get the earliest frame from the queue and send it to the server
        if not frame_queue.empty():
            frame = frame_queue.get()
            encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
            client_socket.sendall(encoded_frame)

# Start thread for capturing frames from the camera
capture_thread = Thread(target=capture_frames)
capture_thread.start()

# Start thread for sending frames to the server
send_thread = Thread(target=send_frames)
send_thread.start()

# Initialize OpenCV window for displaying frames and stats
cv2.namedWindow('Client', cv2.WINDOW_NORMAL)

frame_counter = 0  # Counter for keeping track of the number of frames processed
start_time = time.time()  # Time when processing started

while True:
    if not frame_queue.empty():
        # Get the frame from the queue and display it
        frame = frame_queue.queue[0]

        # Update stats window
        fps = frame_counter / (time.time() - start_time)  # Calculate frame rate
        queue_size = frame_queue.qsize()  # Get number of frames in queue
        stats_text = f'FPS: {fps:.2f}   Queue size: {queue_size}'
        cv2.putText(frame, stats_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow('Client', frame)

        frame_counter += 1

    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
capture_thread.join()
send_thread.join()
client_socket.close()
cv2.destroyAllWindows()
