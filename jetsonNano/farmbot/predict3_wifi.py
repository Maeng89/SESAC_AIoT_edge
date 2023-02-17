import cv2
import numpy as np
from time import sleep
from datetime import datetime

import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
loaded = tf.saved_model.load('./model/converea')


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=800,
    display_height=480,
    framerate= 10,
    flip_method= 0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show():
    num = 0
    window_title = 'aiot'
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
                        
            while True:
                num += 1
                ret_val, frame = video_capture.read()
                
                if frame is None:
                    print('empty frame, reboot please', num)
                    sleep(1)
                else:
                    if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                        cv2.imshow(window_title, frame)
                        try : 
                            #img = cv2.imread(removed)
                            img = frame[0:460, 80:560]
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, (150,150)) / 255.0 # inputµ¥ÀÌÅÍ¸¦ ½ºÄÉÀÏ¸µÇß±â ¶§¹®¿¡ ¿¹ÃøÇÒ ¶§¿¡µµ ½ºÄÉÀÏ¸µ ÇØ¾ßÇÔ
                            
                            pred = loaded([img])
                            pred = np.asarray(pred)
                            growth_level = str(np.argmax(pred, axis=1)[0])
                        
                            print(num, ' growth level', growth_level)
                            
                            client_socket.sendall(growth_level.encode('utf-8'))
                            
                            sleep(0.5)
                            
                            client_response = client_socket.recv(1024).decode()
                            if client_response != 'receive':
                                print('client no response')
                                print('server termination')
                                break
                            print('done')
                            sleep(interval)
                            
                        except Exception as e:
                            print(e)
                            break
                    else:
                        print('????')
# while loop finish line
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord('q'):
                    video_capture.release()
                    cv2.destroyAllWindows()
                    client_socket.close()
                    server_socket.close()
                    sleep(2)
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
            client_socket.close()
            server_socket.close()
            sleep(2)
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    # option
    interval = 2 # sec
    
    # server
    import socket, errno
    HOST = ''
    PORT = 7477
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try :
        print('socket binding start')
        server_socket.bind(('', 7477))
    except socket.err as e:
        if e.errno == errno.EADDRINUSE: # 98 8address already in use
            print(e)
        else :
            print(e)
    
    server_socket.listen()
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    
    client_socket.sendall('connected'.encode())
    
    while True :    
        show()
                                                  
    client_socket.close()
    server_socket.close()
