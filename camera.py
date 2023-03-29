import cv2
import tkinter as tk
from PIL import ImageTk, Image

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Camera")

# Create canvas for camera feed
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

def update_frame():
    # Read frame from camera
    ret, frame = cap.read()

    # Convert frame from OpenCV's BGR format to RGB format for display in Tkinter
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize frame to fit canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    resized_frame = cv2.resize(rgb_frame, (canvas_width, canvas_height))

    # Convert resized frame to PIL format for display in Tkinter
    image = Image.fromarray(resized_frame)

    # Convert PIL image to Tkinter-compatible format and display on canvas
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

    # Call update_frame() function again after 10 milliseconds
    root.after(10, update_frame)

# Call update_frame() function to start updating camera feed
update_frame()

# Add two vertical lines in the middle of the screen
canvas.create_line(canvas.winfo_width()//2, 0, canvas.winfo_width()//2, canvas.winfo_height(), fill='black')
canvas.create_line(canvas.winfo_width()//2 + 1, 0, canvas.winfo_width()//2 + 1, canvas.winfo_height(), fill='black')

# Add two vertical lines in the middle of the screen
line1 = canvas.create_line(canvas.winfo_width()//2, 0, canvas.winfo_width()//2, canvas.winfo_height(), fill='white')
line2 = canvas.create_line(canvas.winfo_width()//2 + 1, 0, canvas.winfo_width()//2 + 1, canvas.winfo_height(), fill='white')

# Bring lines to the front
canvas.tag_raise(line1)
canvas.tag_raise(line2)

# Start Tkinter event loop
root.mainloop()

# Release camera
cap.release()
