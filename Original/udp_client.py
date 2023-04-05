import cv2
import socket
import struct

# create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set the socket address and port
host = '127.0.0.1'
port = 1234

# load the video file
cap = cv2.VideoCapture(0)

# loop through each frame of the video
while cap.isOpened():
    # read the current frame
    ret, frame = cap.read()

    if ret:
        # encode the frame as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, img_encoded = cv2.imencode('.jpg', frame, encode_param)

        # get the size of the encoded frame
        size = len(img_encoded)

        # pack the size and the encoded frame into a struct
        data = struct.pack('>L', size) + img_encoded.tobytes()

        # send the data over the socket
        sock.sendto(data, (host, port))
    else:
        break

# release the resources
cap.release()
sock.close()
