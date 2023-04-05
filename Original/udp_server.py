import cv2
import socket
import struct
import numpy as np

# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set the socket address and port
host = '127.0.0.1'
port = 1234

# bind the socket to the address and port
sock.bind((host, port))

# set the buffer size
buffer_size = 65536


# loop to receive the video stream
while True:
    # receive the data over the socket
    data, addr = sock.recvfrom(buffer_size)

    # unpack the size and image data from the struct
    size = struct.unpack('>L', data[:4])[0]
    img_data = data[4:]

    # decode the JPEG image
    frame = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    # display the frame on the screen
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the resources
sock.close()
cv2.destroyAllWindows()

