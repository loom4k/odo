import cv2
import numpy as np
import random

# Open video capture device
cap = cv2.VideoCapture(0)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define circle parameters
circle_color = (0, 0, 255)  # Red color
circle_radius = 10
circle_thickness = -1  # Filled circle
circle_position = [320, 240]  # Start at the center of the screen

# Define line parameters
y1 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2 - 50
y2 = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2 + 50
line_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) // 3
x1 = int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) - line_width) // 2)
x2 = int(x1 + line_width)

while True:
    # Capture a frame
    ret, frame = cap.read()
    if not ret:
        continue

    # Draw the circle
    cv2.circle(frame, (circle_position[0], circle_position[1]), circle_radius, circle_color, circle_thickness)

    # Move the circle randomly on the x-axis
    circle_position[0] += random.randint(-2, 2)
    circle_position[0] = max(circle_position[0], circle_radius)
    circle_position[0] = min(circle_position[0], frame.shape[1] - circle_radius)

    # Adjust line width based on user input
    if cv2.waitKey(1) & 0xFF == ord('a'):
        y1 += 10
        y2 -= 10
    elif cv2.waitKey(1) & 0xFF == ord('d'):
        y1 -= 10
        y2 += 10

    # Update line coordinates
    x1 = int((frame.shape[1] - line_width) // 2)
    x2 = int(x1 + line_width)

    # Draw two horizontal lines spaced 100 pixels apart and 1/3 the width of the screen
    cv2.line(frame, (x1, int(y1)), (x2, int(y1)), (0, 255, 0), 2)
    cv2.line(frame, (x1, int(y2)), (x2, int(y2)), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
