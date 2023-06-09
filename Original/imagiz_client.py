 Client.py
import imagiz
import cv2


client=imagiz.Client("cc1",server_ip="localhost", server_port=7070) # Connect to server ip on 7070 port
vid=cv2.VideoCapture(0) # capturing webcam frames
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    r,frame=vid.read() # reading captured frame continously for tranmission
    if r:
        r, image = cv2.imencode('.jpg', frame, encode_param) # Encoding captured framed in bytes
        client.send(image) # Sending captured frame over to server side
    else:
        break
'''
-----------------------------------
©著作权归作者所有：来自51CTO博客作者一手代码一手诗的原创作品，请联系作者获取转载授权，否则将追究法律责任
使用Python进行视频帧传输
https://blog.51cto.com/u_14303514/4940421
'''


#Client.py

import imagiz
import cv2
import time
from io import BytesIO
import numpy as np
import base64
import os
import multiprocessing
import signal

def send_webcam(port):
    vid=cv2.VideoCapture(0)
    client=imagiz.Client(server_port=port,client_name="cc1",server_ip='192.168.1.17') # establishing connection with the server computer. Note: change serveer_ip to ip of administrative computer
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # t_end = time.time() + int(time_)
    frame_rate = 10
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        r,frame=vid.read()
        print('Original Dimension', frame.shape)

        if time_elapsed > 1./frame_rate:
            prev = time.time()
            scale_percent = 60 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100) # compressing frame for easy transmission
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA) # resizing frame with provided scale factor

            if r:
                try:
                    r,image=cv2.imencode('.jpg',resized, encode_param) # enconding to bytes

                    np_bytes = BytesIO()

                    np.save(np_bytes, image, allow_pickle=True) # allow_pickle = true allows dimension of numpy array to be encrypted alongside
                    np_bytes = np_bytes.getvalue()

                    en_bytes = base64.b64encode(np_bytes) # base64 encoding of numpy array


                    response=client.send(en_bytes) # sending encoded bytes over to server computer
                    print(response)
                except:
                    break

    vid.release()
    cv2.destroyAllWindows()
    current_id = multiprocessing.current_process().pid
    os.kill(current_id,signal.SIGTERM)

if __name__ == '__main__':
    send_webcam(7070) 
-----------------------------------
©著作权归作者所有：来自51CTO博客作者一手代码一手诗的原创作品，请联系作者获取转载授权，否则将追究法律责任
使用Python进行视频帧传输
https://blog.51cto.com/u_14303514/4940421