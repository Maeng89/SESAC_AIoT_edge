import cv2
import tensorflow as tf
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time
from datetime import datetime

import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Use a service account.
cred = credentials.Certificate('./nugunaaiot-maeng-1004a11a5af7.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


loaded = tf.saved_model.load('./model/converea')


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1900,
    capture_height=1000,
    display_width=800,
    display_height=480,
    framerate=10,
    flip_method=0,
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
    num = 0;
    window_title = 'aiot'
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            

            while True:
                ret_val, frame = video_capture.read()
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                   
##                    img = bgremove3(frame)

                    try : 
                        #img = cv2.imread(removed)
                        img = frame[0:460, 80:560]
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (150,150)) / 255.0 # inputµ¥ÀÌÅÍ¸¦ ½ºÄÉÀÏ¸µÇß±â ¶§¹®¿¡ ¿¹ÃøÇÒ ¶§¿¡µµ ½ºÄÉÀÏ¸µ ÇØ¾ßÇÔ
                        pred = loaded([img])
                        y = np.asarray(pred)
                        y = np.argmax(y, axis=1)
                        num+=1
                        print(num, ' pred', y)
                        upload_pred(y)
                        time.sleep(5)
                    except Exception as e:
                        print(e)
                        pass
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord('q'):
                    video_capture.release()
                    cv2.destroyAllWindows()
                    time.sleep(5)
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
            time.sleep(5)

    else:
        print("Error: Unable to open camera")


d_id = 'd0000002'
def create_device(d_id):
    doc_ref = db.collection('converea').document(d_id)
    doc = doc_ref.get()
    if doc.exists:
        pass
    else:
        doc_ref.set({
            'id': d_id,
            'pred': []
            })
        
def upload_pred(pred):
    doc_ref = db.collection('converea').document(d_id)
    doc_ref.update({'pred' : str(pred) })
##    doc_ref.update({'pred' :  firestore.ArrayUnion([pred]) })

##def bgremove3(myimage):
##    # BG Remover 3
##    myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)
##
##    # Take S and remove any value that is less than half
##    s = myimage_hsv[:, :, 1]
##    s = np.where(s < 127, 0, 1)  # Any value below 127 will be excluded
##
##    # We increase the brightness of the image and then mod by 255
##    v = (myimage_hsv[:, :, 2] + 127) % 255
##    v = np.where(v > 127, 1, 0)  # Any value above 127 will be part of our mask
##
##    # Combine our two masks based on S and V into a single "Foreground"
##    foreground = np.where(s + v > 0, 1, 0).astype(np.uint8)  # Casting back into 8bit integer
##
##    background = np.where(foreground == 0, 255, 0).astype(np.uint8)  # Invert foreground to get background in uint8
##    background = cv2.cvtColor(background, cv2.COLOR_GRAY2RGB)  # Convert background back into BGR space
##    foreground = cv2.bitwise_and(myimage, myimage, mask=foreground)  # Apply our foreground map to original image
##    finalimage = background + foreground  # Combine foreground and background
##    return finalimage








if __name__ == "__main__":
    create_device(d_id)
##    doc_ref = db.collection('converea').document(d_id)

    show()    


    




