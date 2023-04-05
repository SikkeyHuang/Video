import socket
import cv2
import numpy as np
import time

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
    data = img_encoded.tobytes()
    #data = img_encoded.tostring()

    # Send the frame to the server
    start_time = time.time()
    client_socket.sendall(data)
    
    # Delay to control the frame rate
    elapsed_time = time.time() - start_time
    delay = 1 / frame_rate - elapsed_time
    if delay > 0:
        time.sleep(delay)

    # Delay to control the frame rate
    #time.sleep(1 / frame_rate)

# Clean up
client_socket.close()
camera.release()
cv2.destroyAllWindows()
