
import cv2
import numpy as np
import cvzone
import pickle

WIDTH, HEIGHT = 50, 105
pos_list = []

        # ESP32 camera URL
camera_url = "http://192.168.1.114:81/stream"

def resize_image(image):
    
    # Get the origiinal image dimensions
    height, width = image.shape[:2]

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Set the target size
    target_size = (600, 600)

    # Determine the resize dimensions based on the aspect ratio
    if aspect_ratio > 1:
        new_width = target_size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = target_size[1]
        new_width = int(new_height * aspect_ratio)

    # Resize the image while maintaining the aspect ratio
    resized_image = cv2.resize(image, (new_width, new_height))

    # Create a black canvas of the target size
    canvas = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)

    # Calculate the position to paste the resized image
    x = int((target_size[0] - new_width) / 2)
    y = int((target_size[1] - new_height) / 2)

    # Paste the resized image onto the canvas
    canvas[y:y + new_height, x:x + new_width] = resized_image

    return canvas

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos  in enumerate(pos_list):
            x1, y1 = pos
            if x1<x<x1+WIDTH and y1<y<y1+HEIGHT:
                pos_list.pop(i)
    
    with open('CarparkPos', 'wb') as f:
        # pickle.dump([(96, 248), (145, 248), (259, 248), (308, 247), (410, 248), (459, 248), (509, 249)], f)
        pickle.dump(pos_list, f)
        

try:
    with open('CarparkPos', 'rb') as f:
        pos_list = pickle.load(f)
except:
    pos_list = []

def main():

    # cap = cv2.VideoCapture(camera_url)
    cap = cv2.VideoCapture('VID2.mp4')

    while True:

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
        ret, frame = cap.read()
        # image = cv2.imread(frame)
        # Resize the image
        resized_image = resize_image(frame)

        imgGray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 11) # can play around 2nd to the last and last values. Only odd numbers allowed

        imgMedian = cv2.medianBlur(imgThreshold, 5)


        kernel = np.ones((3,3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        for pos in pos_list:
            x, y = pos

            img_crop = imgDilate[y:y+HEIGHT, x:x+WIDTH]
            # cv2.imshow(str(x*y), img_crop)
            count = cv2.countNonZero(img_crop)
            # print(count)
            cvzone.putTextRect(resized_image, str(count), (x,y+HEIGHT-4), scale=1, thickness= 1, offset= 0, colorR=(0,0,255))

            if count < 800:
                color = (0,255,0)
                thickness = 5
            else:
                color = (0,0,255)
                thickness = 2
            cv2.rectangle(resized_image, pos, (pos[0]+WIDTH,pos[1]+HEIGHT), color, thickness)
            # cv2.rectangle(resized_image, pos, (pos[0]+WIDTH,pos[1]+HEIGHT), (255,0,255), 2)

        
        # Display the resized image
        cv2.imshow('Resized Image', resized_image)
        # cv2.imshow('Blur', imgBlur)
        # cv2.imshow('Image Threshold', imgThreshold)
        # cv2.imshow('Image Median', imgMedian)
        # cv2.setMouseCallback("Resized Image", mouseClick)
        cv2.waitKey(1)
        # cv2.destroyAllWindows()
main()



