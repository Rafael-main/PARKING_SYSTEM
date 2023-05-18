import cv2

# def capture_image(video_path = r"app\assets\Thesis video\VID_20230228_115522.mp4"):
def capture_image(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error: Could not open video file")
        return None

    # Read the first frame of the video
    ret, frame = cap.read()

    # Check if a frame was successfully read
    if not ret:
        print("Error: Could not read frame from video file")
        return None

    # Release the video capture object
    cap.release()

    # Return the captured image

    cv2.imshow("image", frame)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return frame

def main():
    # define width and height
    WIDTH, HEIGHT = 470, 500

    # position list
    posList = []

    def mouseClickEvents(events, x, y, flags, params) :
        if events == cv2.EVENT_LBUTTONDOWN:
            posList.append((x,y))

    # capture frame
    frame = capture_image("VID2.mp4")
    # img = cv2.imread(frame)

    while True:
        # cv2.rectangle(frame, (920, 800), (450,300), (255,0,255), 2)

        # find position
        for pos in posList:
            cv2.rectangle(frame, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)

        cv2.imshow("image", frame)
        cv2.waitKey(1)
    # cv2.destroyAllWindows()


main()
# frame = capture_image()
# img = cv2.imread("car_one.png")

# while True:

#     cv2.imshow("image", img)
#     cv2.waitKey(1)
    