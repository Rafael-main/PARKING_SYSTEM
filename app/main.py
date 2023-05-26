import datetime
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

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



    def update_datetime(self):
        # Update date/time label
        now = datetime.datetime.now()
        self.datetime_label.config(text=now.strftime("%m/%d/%Y %H:%M:%S"))

        # Restart timer
        self.left_frame.after(5000, self.update_datetime)

class carParkDetect: 
    def resize_image(image):
        # Get the original image dimensions
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


    def detect_parking_spots(self, image):
        # to be run by image processing class
        return None

    

    # Step 2: Preprocess Images
    def preprocess_image(self, frame):
        # Convert to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur to reduce noise
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        return blurred_image

    # Step 3: Define a Reference Image
    reference_image = cv2.imread('reference_image.jpg')

    # Step 4: Background Subtraction
    def perform_background_subtraction(self, reference_image, current_frame):
        # Perform background subtraction
        diff_image = cv2.absdiff(reference_image, current_frame)

        return diff_image

    # Step 5: Thresholding
    def apply_thresholding(self, diff_image):
        # Convert to grayscale
        gray_image = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        _, thresholded_image = cv2.threshold(self, gray_image, 20, 255, cv2.THRESH_BINARY)

        return thresholded_image

    # Step 6: Morphological Operations
    def perform_morphological_operations(self, thresholded_image):
        # Perform morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated_image = cv2.dilate(thresholded_image, kernel, iterations=2)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1)

        return eroded_image

    # Step 7: Contour Detection
    def find_contours(self, eroded_image):
        # Find contours
        contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    # Step 8: Parking Space Detection
    def detect_parking_spaces(self, current_frame, contours):
        for contour in contours:
            # Calculate contour area
            area = cv2.contourArea(contour)

            # Set a threshold for minimum contour area
            if area > 5000:
                # Draw a bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return current_frame
    def main(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            preprocessed_frame = self.preprocess_image(frame)
            diff_image = self.perform_background_subtraction(self.reference_image, preprocessed_frame)
            thresholded_image = self.apply_thresholding(diff_image)

            eroded_image = self.perform_morphological_operations(thresholded_image)

            contours = self.find_contours(eroded_image)

            result = self.detect_parking_spaces(frame, contours)

            cv2.imshow('Parking Detection', result)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

root = tk.Tk()
app = ParkingApp(root)
root.mainloop()
