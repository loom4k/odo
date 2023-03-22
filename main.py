import tkinter as tk

root = tk.Tk()

# Set the window size to full screen
root.attributes('-fullscreen', True)

# Create a frame for the top section (white)
top_frame = tk.Frame(root, bg='white')
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame for the bottom section (white)
bottom_frame = tk.Frame(root, bg='white')
bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.update_idletasks()

# Create the labels and text inputs in the left frame
label_names = [
    "Largeur de la cible", 
    "IBO", 
    "Distance de flexion", 
    "Poids supp. sur la corde", 
    "Force de tension", 
    "Poids de la fleche", 
]
input_boxes = []  # list to hold the text input widgets
selected_input = None  # variable to hold the currently selected text input

def select_input(widget):
    widget.delete(0, tk.END)
    # This function is called when a text input widget is clicked
    global selected_input
    selected_input = widget

def set_placeholder(i):
    text_input.config(fg="grey")
    if i == 0:
        text_input.insert(0, "Ex: 80 (cm)")
    elif i == 1:
        text_input.insert(0, "Ex: 200 (fps)")
    elif i == 2:
        text_input.insert(0, "Ex: 1.65 (m)")
    elif i == 3:
        text_input.insert(0, "Ex: 55658 (grains)")
    elif i == 4:
        text_input.insert(0, "Ex: 20 (lbs)")
    elif i == 5:
        text_input.insert(0, "Ex: 750 (grains)")

for i in range(len(label_names)):
    label = tk.Label(top_frame, text=label_names[i], font=("Arial", 18), padx=5, pady=(25/2), bg="white")
    label.grid(row=i, column=0, sticky="w")
    text_input = tk.Entry(top_frame, font=("Arial", 18), insertontime=0, insertofftime=500)
    set_placeholder(i)
    text_input.grid(row=i, column=1, padx=5, pady=5)
    input_boxes.append(text_input)
    text_input.bind("<Button-1>", lambda event, widget=text_input: select_input(widget))

root.mainloop()
