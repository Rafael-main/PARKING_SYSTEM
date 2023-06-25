import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import pickle
import cvzone
import threading
import time

class ParkingTable:
    def __init__(self, master):
        self.master = master
        self.create_table()

    def read_occupants(self):
        with open('integer.pickle', 'rb') as file:
            loaded_integer = pickle.load(file)
            file.close()
        return loaded_integer
    
    def read_pos_stats(self):
        list_pos_stats = []
        with open('PosStats.pickle', 'rb') as file:
            pos_stats = pickle.load(file)
            file.close()
        for i in pos_stats:
            list_pos_stats.append(pos_stats[i]['status'])
        return list_pos_stats
        
    def create_table(self):
        #  Create date/time label
        # create headers
        headers = ["Parking Slot Number", "Availability", "Actions"]
        for i, header in enumerate(headers):
            label = tk.Label(self.master, text=header, relief=tk.RIDGE, width=20)
            label.grid(row=0, column=i)

        self.read_pos_stats()
        # create rows
        with open('CarparkPos', 'rb') as file:
            list_of_all_pos = pickle.load(file)
            file.close()
        self.is_parked_values = ["No"] * len(list_of_all_pos)  # initialize all values to "No"

        self.is_parked_values = self.read_pos_stats()
        print(f'ANG ANIMAL {self.is_parked_values}')

        for i in range(1, (len(list_of_all_pos) + 1)):
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
        
        self.master.after(2000, self.create_table)

    def change_parked(self, slot_number, value):
        self.is_parked_values[slot_number] = value
        row = slot_number + 1
        is_parked_label = self.master.grid_slaves(row=row, column=1)[0]
        is_parked_label.config(text=value)

    def change_parked_detection(self, slot_number, value):
        self.is_parked_values[slot_number] = value
        row = slot_number + 1
        is_parked_label = self.master.grid_slaves(row=row, column=1)[0]
        is_parked_label.config(text=value)

class ParkingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Parking App")

        # create left and right frames
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10)
        right_frame = tk.Frame(self.master)
        right_frame.pack(side=tk.RIGHT, padx=10)

        # add date time
        self.datetime_label = tk.Label(self.left_frame, font=("Arial", 16))
        self.datetime_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.mlem = tk.Label(self.left_frame, textvariable='qweqwe',font=("Arial", 16))
        self.mlem.grid(row=0, column=0, padx=10, pady=10)

        # add table on left frame
        table = ParkingTable(self.left_frame)



class DetectionSystem:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 75, 175
        self.pos_list = []
        self.pos_stats = {}

        # ESP32 camera URL
        self.camera_url = "http://192.168.1.121:81/stream"
        self.camera_url = "VID1.mp4"

        self.spaceCounter = 0

    def save_occupants(self, numOfOccu):
        with open('integer.pickle', 'rb+') as file:
            pickle.dump(numOfOccu, file)
            file.truncate()

        file.close()

    def save_is_pos_available(self, posStatus):
        with open('PosStats.pickle', 'rb+') as file:
            pickle.dump(posStatus, file)
            file.truncate()

        file.close()

    def read_pos_stats(self):
        with open('PosStats.pickle', 'rb') as file:
            pos_stats = pickle.load(file)
            file.close()
        print(pos_stats)
        self.pos_stats = pos_stats

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


        if self.pos_list != []:
            initialPosStats = {}
            for i in range(1, (len(self.pos_list) + 1)):
                initialPosStats[self.pos_list[i-1]] = {'Position':f'POSITION {i}','status':'No'}
            print(initialPosStats)
            self.save_is_pos_available(initialPosStats)
        
        self.read_pos_stats()

        cap = cv2.VideoCapture(self.camera_url)

        # image = cv2.imread('nye.png')
        while True:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
            ret, frame = cap.read()
            # # Resize the image
            resized_image = self.resize_image(frame)

            imgGray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 11) # can play around 2nd to the last and last values. Only odd numbers allowed

            imgMedian = cv2.medianBlur(imgThreshold, 5)


            kernel = np.ones((3,3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)


            occuCounter = 0
            for pos in self.pos_list:
                x, y = pos

                img_crop = imgDilate[y:y+self.HEIGHT, x:x+self.WIDTH]
                # cv2.imshow(str(x*y), img_crop)
                count = cv2.countNonZero(img_crop)
                # print(count)
                cvzone.putTextRect(resized_image, str(count), (x,y+self.HEIGHT-4), scale=1, thickness= 1, offset= 0, colorR=(0,0,255))

                if count < 2200:
                    color = (0,255,0)
                    thickness = 5
                    self.spaceCounter += 1
                    occuCounter += 1
                    print(pos)
                else:
                    color = (0,0,255)
                    thickness = 2
                    print(pos)
                    self.pos_stats[pos]['status'] = 'Yes'
                    time.sleep(1)
                cv2.rectangle(resized_image, pos, (pos[0]+self.WIDTH,pos[1]+self.HEIGHT), color, thickness)
            self.save_occupants(occuCounter)
            self.save_is_pos_available(self.pos_stats)
            print(self.pos_stats)
            cvzone.putTextRect(resized_image, str(f'Free: {self.spaceCounter} of {len(self.pos_list)}'), (50,50), scale=2, thickness= 2, offset= 10, colorR=(0,200,0))


            
            # Display the resized image
            cv2.imshow('Parking detection system', resized_image)
            # cv2.imshow('Blur', imgBlur)
            # cv2.imshow('Image Threshold', imgThreshold)
            # cv2.imshow('Image Median', imgMedian)
            # cv2.setMouseCallback("Resized Image", self.mouseClick)
            if cv2.waitKey(25) & 0xFF == ord('q'):
              break
            # cv2.waitKey(10)
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