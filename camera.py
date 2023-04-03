import cv2

color = (0, 0, 0) # Define the color of the lines
thickness = 2 # Define the thickness of the lines
line_distance = 50 # Initialize the line distance
cap = cv2.VideoCapture(0) # Initialize the camera capture

# Variables for formula of the equation
b = 0 # Distance of the bow from the ground

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Unable to open camera")
    exit()

# Create the window and set its properties
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("Unable to capture frame")
        break

    # Rotate the frame by 90 degrees clockwise
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # Get the height and width of the rotated frame
    height, width = frame.shape[:2]

    # Define the position of the center line
    center_x = width // 2
    center_y = height // 2

    # Define the position of the lines with the adjusted distance
    left_x = center_x - line_distance
    right_x = center_x + line_distance
    line_y = height // 4

    # Draw the lines on top of the frame with the adjusted distance
    cv2.line(frame, (left_x, line_y), (left_x, height - line_y), color, thickness)
    cv2.line(frame, (right_x, line_y), (right_x, height - line_y), color, thickness)

    # Display the resulting frame only if the window is still open
    if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) > 0:
        cv2.imshow('Camera', frame)

    # Check for keyboard input
    key = cv2.waitKeyEx(1)
    if key == ord('q'):
        break
    elif key == ord('a'):  # Left arrow key
        line_distance = max(line_distance - 5, 0)  # Decrease line distance by 5, but allow it to be 0
    elif key == ord('d'):  # Right arrow key
        line_distance += 5  # Increase line distance by 5
    elif key == ord(' '):  # Space key
        print("Distance between lines:", abs(left_x - right_x))

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
