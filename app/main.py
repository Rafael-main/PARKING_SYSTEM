import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2

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
        self.video_source = video_soruce

        self.video_capture = cv2.VideoCapture(video_source)

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


    def detect_parking_spots(self, image):
        # to be run by image processing class
       
        # ret, frame = self.video_capture.read()
        # if ret:
        #     cv2.imwrite("captured_frame.jpg", frame)
        #     print("Frame captured!")
        # return image
        return None
    
    def update(self):
        # Get the latest frame and convert it to PIL Image format
        ret, frame = self.video_capture.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            self.photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(15, self.update)  # Refresh the frame every 15 milliseconds

    def update_datetime(self):
        # Update date/time label
        now = datetime.datetime.now()
        self.datetime_label.config(text=now.strftime("%m/%d/%Y %H:%M:%S"))

        # Restart timer
        self.left_frame.after(5000, self.update_datetime)

root = tk.Tk()
app = ParkingApp(root)
root.mainloop()
