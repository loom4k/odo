import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)

# Create the left frame to hold the labels and text inputs
left_frame = tk.Frame(root, bg="white", width=300, height=root.winfo_screenheight())
left_frame.pack(side="left", fill="both", expand=True)

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
    label = tk.Label(left_frame, text=label_names[i], font=("Arial", 18), padx=5, pady=10, bg="white")
    label.grid(row=i, column=0, sticky="w")
    text_input = tk.Entry(left_frame, font=("Arial", 18), insertontime=0, insertofftime=500)
    set_placeholder(i)
    text_input.grid(row=i, column=1, padx=5, pady=5)
    input_boxes.append(text_input)
    text_input.bind("<Button-1>", lambda event, widget=text_input: select_input(widget))

# Create the submit button
submit_button = tk.Button(left_frame, text="Submit", font=("Arial", 18), command=lambda: submit_inputs())
submit_button.grid(row=len(label_names)+2, column=0, pady=10, padx=35)

# Create an exit button
exit_button = tk.Button(left_frame, text="Exit", font=("Arial", 18), command=root.quit)
exit_button.grid(row=len(label_names)+2, column=1, pady=10)

# Create the right frame to hold the number pad and submit button
right_frame = tk.Frame(root, bg="white", width=300, height=root.winfo_screenheight())
right_frame.pack(side="right", fill="both", expand=True)

# Define a function to handle button clicks
def button_click(number):
    # Insert the clicked number into the currently selected text input widget
    if selected_input:
        selected_input.insert(tk.END, number)

# Create a grid of buttons to form the number pad
for i in range(1, 10):
    button = tk.Button(right_frame, text=str(i), font=("Arial", 28), command=lambda num=i: button_click(num))
    button.grid(row=(i-1)//3, column=(i-1)%3, padx=10, pady=10, sticky="nsew")

# Create a dot button
button_dot = tk.Button(right_frame, text=".", font=("Arial", 28), command=lambda: button_click("."))
button_dot.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Create a button for zero
button_zero = tk.Button(right_frame, text="0", font=("Arial", 28), command=lambda: button_click(0))
button_zero.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Create a delete button
button_delete = tk.Button(right_frame, text="←", font=("Arial", 28), command=lambda: [widget.delete(len(widget.get())-1) for widget in input_boxes if widget==selected_input])
button_delete.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# Create a button to clear all the text inputs
button_clear = tk.Button(right_frame, text="Clear", font=("Arial", 18), command=lambda: [widget.delete(0, tk.END) for widget in input_boxes])
button_clear.grid(row=4, column=1, pady=10)

def submit_inputs():
    # Get the values from the text input widgets and print them
    values = [widget.get() for widget in input_boxes]
    print(values)

root.mainloop()