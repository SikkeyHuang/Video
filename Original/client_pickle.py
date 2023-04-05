import socket
import cv2
import pickle
import struct
import threading
import time
from queue import Queue


# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Initialize camera
camera = cv2.VideoCapture(0)

# Set desired frame rate (in frames per second)
frame_rate = 10

while True:
    # Capture a frame from the camera
    ret, frame = camera.read()
    if not frame:
        break
    # Convert frame to bytes for transmission
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, img_encoded = cv2.imencode('.jpg', frame, encode_param)

    # Serialize the frame and send it to the server
    frame_data = pickle.dumps(img_encoded)

    size = len(frame_data)
    client_socket.sendall(struct.pack(">L", size) + frame_data)

    # frame_data = pickle.dumps(img_encoded)
    # msg_size = struct.pack("Q", len(frame_data))
    #client_socket.send(msg_size + frame_data)

# Clean up
client_socket.close()
camera.release()
cv2.destroyAllWindows()


