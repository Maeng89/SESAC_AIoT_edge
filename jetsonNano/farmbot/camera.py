import cv2
import tensorflow as tf
import numpy as np


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
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
     
##                    try : 
##                        img = cv2.imread(removed)
##                        img = img[60:420, :420]
##                        img = cv2.resize(img, (150,150)) / 255.0 # inputµ¥ÀÌÅÍ¸¦ ½ºÄÉÀÏ¸µÇß±â ¶§¹®¿¡ ¿¹ÃøÇÒ ¶§¿¡µµ ½ºÄÉÀÏ¸µ ÇØ¾ßÇÔ
##                        pred = loaded([img])
##                        y = np.asarray(pred)
##                        y = np.argmax(y, axis=1)
##                        num+=1
##                        print(num)
##                        print(y)
##                    except Exception as e:
##                        print(e)
##                        pass
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")










if __name__ == "__main__":
    show()    


    




