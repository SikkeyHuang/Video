import socket
import cv2
import pickle
import struct
from queue import Queue
import threading

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

    '''
    data = b''
    payload_size = struct.calcsize("Q")
    while True:
        # Receive data from client and add it to buffer
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4 KB buffer
            if not packet:
                break
            data += packet

        # Extract message size and deserialize message data
        if len(data) >= payload_size:
            msg_size = struct.unpack("Q", data[:payload_size])[0]
            data = data[payload_size:]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)  # 4 KB buffer
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Deserialize message data to get the frame
            frame = pickle.loads(frame_data)
    '''

    data = b""
    payload_size = struct.calcsize(">L")
    #print("payload_size: {}".format(payload_size))

    while True:
        # Receive frame from client
        while len(data) < payload_size:
            #print("Recv: {}".format(len(data)))
            data += client_socket.recv(4096)

        #print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        #print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        #print("data_size: {}".format(data))
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)
        cv2.waitKey(1)

        # Display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Close the client socket
    client_socket.close()

# Clean up
server_socket.close()
cv2.destroyAllWindows()





