import cv2
import numpy as np

# Open video capture device
cap = cv2.VideoCapture(0)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
