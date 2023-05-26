import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import pickle
import cvzone
import threading

class ParkingTable:
    def __init__(self, master):
        self.master = master
        self.create_table()

        
    def create_table(self):
        #  Create date/time label
        # create headers
        headers = ["Parking Slot Number", "Is Parked", "Actions"]
        for i, header in enumerate(headers):
            label = tk.Label(self.master, text=header, relief=tk.RIDGE, width=20)
            label.grid(row=0, column=i)

        # create rows
        self.is_parked_values = ["No"] * 10  # initialize all values to "No"
        for i in range(1, 11):
            # add date, time, and parking slot number
            # date_label = tk.Label(self.master, text="2023-03-30", relief=tk.RIDGE, width=20)
            # date_label.grid(row=i, column=0)
            # time_label = tk.Label(self.master, text="10:00", relief=tk.RIDGE, width=20)
            # time_label.grid(row=i, column=1)
            slot_label = tk.Label(self.master, text=str(i), relief=tk.RIDGE, width=20)
            slot_label.grid(row=i, column=0)

            # add is parked label
            is_parked_label = tk.Label(self.master, text=self.is_parked_values[i-1], relief=tk.RIDGE, width=20)
            is_parked_label.grid(row=i, column=1)

            # add actions buttons
            yes_button = tk.Button(self.master, text="Yes", width=8, command=lambda i=i: self.change_parked(i-1, "Yes"))
            yes_button.grid(row=i, column=2)
            no_button = tk.Button(self.master, text="No", width=8, command=lambda i=i: self.change_parked(i-1, "No"))
            no_button.grid(row=i, column=3)

    def change_parked(self, slot_number, value):
        self.is_parked_values[slot_number] = value
        row = slot_number + 1
        is_parked_label = self.master.grid_slaves(row=row, column=1)[0]
        is_parked_label.config(text=value)

class ParkingApp:
    def __init__(self, master, video_soruce=0):
        self.master = master
        self.master.title("Parking App")

        # create left and right frames
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10)
        right_frame = tk.Frame(self.master)
        right_frame.pack(side=tk.RIGHT, padx=10)

        # add image on right frame
        img = Image.open("example_image.jpg")
        img = img.resize((400, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(right_frame, image=photo)
        label.image = photo
        label.pack()
        
        img2 = Image.open("example_image.jpg")
        img2 = img.resize((400, 400), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(img2)
        label2 = tk.Label(right_frame, image=photo2)
        label2.image = photo2
        label2.pack()

        # add date time
        self.datetime_label = tk.Label(self.left_frame, font=("Arial", 16))
        self.datetime_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.mlem = tk.Label(self.left_frame, textvariable='qweqwe',font=("Arial", 16))
        self.mlem.grid(row=0, column=0, padx=10, pady=10)

        # add table on left frame
        table = ParkingTable(self.left_frame)



class DetectionSystem:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 50, 105
        self.pos_list = []

        # ESP32 camera URL
        # self.camera_url = "http://192.168.1.27:81/stream"

    def resize_image(self, image):
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

    def mouseClick(self, events, x, y, flags, params):
    # def mouseClick():
        if events == cv2.EVENT_LBUTTONDOWN:
            self.pos_list.append((x,y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for pos, i in enumerate(self.pos_list):
                x1, y1 = pos
                if x1<x<x1+self.WIDTH and y1<y<y1+self.HEIGHT:
                    self.pos_list.pop(i)
        
        with open('CarparkPos', 'wb') as f:
            # pickle.dump([(96, 248), (145, 248), (259, 248), (308, 247), (410, 248), (459, 248), (509, 249)], f)
            pickle.dump(self.pos_list, f)
        

    def main(self):
        try:
            with open('CarparkPos', 'rb') as f:
                self.pos_list = pickle.load(f)
        except:
            self.pos_list = []

        # cap = cv2.VideoCapture(self.camera_url)
 
        # # Check if camera opened successfully
        # if (cap.isOpened()== False): 
        #   print("Error opening video stream or file")
        
        # # Read until video is completed
        # while(cap.isOpened()):
        #   # Capture frame-by-frame
        #   ret, frame = cap.read()
        #   if ret == True:
        
        #     # Display the resulting frame
        #     res_frame = self.resize_image(frame)
        #     cv2.imshow('Frame',res_frame)
        
        #     # Press Q on keyboard to  exit
        #     if cv2.waitKey(25) & 0xFF == ord('q'):
        #       break
        
        #   # Break the loop
        #   else: 
        #     break
        
        # # When everything done, release the video capture object
        # cap.release()

        image = cv2.imread('nye.png')
        while True:
            # Resize the image
            resized_image = self.resize_image(image)

            imgGray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 11) # can play around 2nd to the last and last values. Only odd numbers allowed

            imgMedian = cv2.medianBlur(imgThreshold, 5)


            kernel = np.ones((3,3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            for pos in self.pos_list:
                x, y = pos

                img_crop = imgDilate[y:y+self.HEIGHT, x:x+self.WIDTH]
                # cv2.imshow(str(x*y), img_crop)
                count = cv2.countNonZero(img_crop)
                # print(count)
                cvzone.putTextRect(resized_image, str(count), (x,y+self.HEIGHT-4), scale=1, thickness= 1, offset= 0, colorR=(0,0,255))

                if count < 1100:
                    color = (0,255,0)
                    thickness = 5
                else:
                    color = (0,0,255)
                    thickness = 2
                cv2.rectangle(resized_image, pos, (pos[0]+self.WIDTH,pos[1]+self.HEIGHT), color, thickness)

            
            # Display the resized image
            cv2.imshow('Resized Image', resized_image)
            # cv2.imshow('Blur', imgBlur)
            # cv2.imshow('Image Threshold', imgThreshold)
            # cv2.imshow('Image Median', imgMedian)
            # cv2.setMouseCallback("Resized Image", mouseClick)
            cv2.waitKey(1)
            # cv2.destroyAllWindows()


# app
def run_app():
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
# run_app()

# detection system
def run_system():
    detect_cars = DetectionSystem()
    return detect_cars.main()
# run_system()


if __name__ == "__main__":
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    detect_park_thread = threading.Thread(target=run_system)
    detect_park_thread.start()



# # ESP32 camera URL
# camera_url = "http://192.168.1.27:81/stream"

# def resize_image(image):
#     # Get the original image dimensions
#     height, width = image.shape[:2]

#     # Calculate the aspect ratio
#     aspect_ratio = width / height

#     # Set the target size
#     target_size = (600, 600)

#     # Determine the resize dimensions based on the aspect ratio
#     if aspect_ratio > 1:
#         new_width = target_size[0]
#         new_height = int(new_width / aspect_ratio)
#     else:
#         new_height = target_size[1]
#         new_width = int(new_height * aspect_ratio)

#     # Resize the image while maintaining the aspect ratio
#     resized_image = cv2.resize(image, (new_width, new_height))

#     # Create a black canvas of the target size
#     canvas = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)

#     # Calculate the position to paste the resized image
#     x = int((target_size[0] - new_width) / 2)
#     y = int((target_size[1] - new_height) / 2)

#     # Paste the resized image onto the canvas
#     canvas[y:y + new_height, x:x + new_width] = resized_image

#     return canvas
# # Create a VideoCapture object and read from input file
# # If the input is the camera, pass 0 instead of the video file name
# cap = cv2.VideoCapture(camera_url)
 
# # Check if camera opened successfully
# if (cap.isOpened()== False): 
#   print("Error opening video stream or file")
 
# # Read until video is completed
# while(cap.isOpened()):
#   # Capture frame-by-frame
#   ret, frame = cap.read()
#   if ret == True:
 
#     # Display the resulting frame
#     res_frame = resize_image(frame)
#     cv2.imshow('Frame',res_frame)
 
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break
 
#   # Break the loop
#   else: 
#     break
 
# # When everything done, release the video capture object
# cap.release()
 
# # Closes all the frames
# cv2.destroyAllWindows()