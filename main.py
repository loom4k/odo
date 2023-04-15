import cv2

# Open video capture device
cap = cv2.VideoCapture(0)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Draw two vertical lines in the middle of the screen
    y1 = frame.shape[0] // 2 - 50
    y2 = frame.shape[0] // 2 + 50
    line_width = frame.shape[1] // 3
    x1 = (frame.shape[1] - line_width) // 2
    x2 = x1 + line_width
    cv2.line(frame, (x1, y1), (x2, y1), (0, 255, 0), 2)
    cv2.line(frame, (x1, y2), (x2, y2), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
