import tkinter as tk

root = tk.Tk()

# Set the window size to full screen
root.attributes('-fullscreen', True)

# Create a frame for the top section (white)
top_frame = tk.Frame(root, bg='white', height=root.winfo_screenheight()//2, )
top_frame.pack(side=tk.TOP, fill=tk.BOTH)

margin_frame = tk.Frame(root, bg='white', height=150)
margin_frame.pack(side=tk.TOP, fill=tk.BOTH)

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

# Create the buttons for the number pad
button_list = [
    '1', '2', '3',
    '4', '5', '6',
    '7', '8', '9',
    '.', '0', 'C'
]

# Create and place the buttons in the bottom frame
for i in range(len(button_list)):
    button = tk.Button(bottom_frame, text=button_list[i], width=5, height=3, command=lambda num=i: button_click(num))
    button.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="NSEW")
    
# Add the following code to center the frame
for j in range(3):
    bottom_frame.columnconfigure(j, weight=1)
    bottom_frame.rowconfigure(4, weight=1)


# Create an exit button
exit_button = tk.Button(margin_frame, text="Exit", font=("Arial", 18), command=root.quit)
exit_button.pack(side=tk.RIGHT, padx=75, pady=50, anchor=tk.CENTER)

# Create the submit button
submit_button = tk.Button(margin_frame, text="Submit", font=("Arial", 18), command=lambda: submit_inputs())
submit_button.pack(side=tk.LEFT, padx=75, pady=50, anchor=tk.CENTER)

# Define a function to handle button clicks
def button_click(number):
    # Insert the clicked number into the currently selected text input widget
    if number == 9:
        selected_input.insert(tk.END, ".")
    elif number == 10:
        selected_input.insert(tk.END, "0")
    elif number == 11:
        selected_input.delete(0, tk.END)
    elif selected_input:
        selected_input.insert(tk.END, number + 1)

def submit_inputs():
    # Get the values from the text input widgets and print them
    values = [widget.get() for widget in input_boxes]
    print(values)
    from AngleOMeter import run_camera_window
    run_camera_window()

root.mainloop()