import cv2

# set screen resolution
screen_width = 800
screen_height = 480

# open camera
cap = cv2.VideoCapture(0)

# set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# create full screen window
cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    
    if ret:
        # display frame in window
        cv2.imshow("Camera", frame)
    
    # break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release camera and close window
cap.release()
cv2.destroyAllWindows()
