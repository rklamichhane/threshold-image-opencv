import cv2 as cv
import numpy as np
import time
 
# Do nothing callback function
def do_nothing(*args, **kwargs):
    pass
 
# Function to return current position of trackbars
def get_trackbar_pos():
    low_H = cv.getTrackbarPos('Low H','Trackbars')
    high_H = cv.getTrackbarPos('High H','Trackbars')
    
    low_S = cv.getTrackbarPos('Low S','Trackbars')
    high_S = cv.getTrackbarPos('High S','Trackbars')
    
    low_V = cv.getTrackbarPos('Low V','Trackbars')
    high_V = cv.getTrackbarPos('High V','Trackbars')
    
    return low_H,high_H, low_S, high_S, low_V, high_V


if __name__ == '__main__':
    
    # Create window named Trackbars to hold multiple trackbars.
    cv.namedWindow('Trackbars')
    cv.namedWindow('Real Image')
    cv.namedWindow('Threshold Image')
    cv.createTrackbar('Low H', 'Trackbars' , 0, 180, do_nothing)
    cv.createTrackbar('High H', 'Trackbars' , 14, 180, do_nothing)
    cv.createTrackbar('Low S', 'Trackbars' , 124, 255, do_nothing)
    cv.createTrackbar('High S', 'Trackbars' , 255, 255, do_nothing)
    cv.createTrackbar('Low V', 'Trackbars' , 152, 255, do_nothing)
    cv.createTrackbar('High V', 'Trackbars' , 255, 255, do_nothing)
    
    #Video Capture object
    cap = cv.VideoCapture(0)

    try:
        # Loop over frames
        while True:
            ret,frame = cap.read()
            if frame is None:
                print("hola")
                break
            # Lets do some image pre-processing
            blurred_frame = cv.GaussianBlur(frame, (11, 11), 0)
            frame_HSV = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
            # Reading from trackbars
            low_H,high_H, low_S, high_S, low_V, high_V  = get_trackbar_pos()

            # Threshold image after thresholding
            threshold_frame = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

            # More of image processing to remove noise
            threshold_frame = cv.erode(threshold_frame ,None,iterations = 2)
            threshold_frame = cv.dilate(threshold_frame ,None,iterations=2)
            # Time for show
            cv.imshow('Real Image',frame)
            cv.imshow('Threshold Image',threshold_frame)
            # wait 30ms for key to be pressed
            # if pressed key is not 'q' or ESC continue to loop
            key = cv.waitKey(30)
            if key == ord('q') or key == 27:
                cv.destroyAllWindows()
                cap.release()
                break
    # On any exception its good practice to release resources. 
    except Exception as e:
        cv.destroyAllWindows()
        cap.release()
        raise e
