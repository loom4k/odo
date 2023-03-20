import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)

# Create the left frame to hold the labels and text inputs
left_frame = tk.Frame(root, bg="white", width=300, height=root.winfo_screenheight())
left_frame.pack(side="left", fill="both", expand=True)

root.update_idletasks()

# Create the labels and text inputs in the left frame
label_names = ["Input 1", "Input 2", "Input 3", "Input 4", "Input 5", "Input 6", "Input 7", "Input 8"]
input_boxes = []  # list to hold the text input widgets
selected_input = None  # variable to hold the currently selected text input

def select_input(widget):
    # This function is called when a text input widget is clicked
    global selected_input
    selected_input = widget

for i in range(len(label_names)):
    label = tk.Label(left_frame, text=label_names[i], font=("Arial", 14), padx=5, pady=5)
    label.grid(row=i, column=0, sticky="w")
    text_input = tk.Entry(left_frame, font=("Arial", 14))
    text_input.grid(row=i, column=1, padx=5, pady=5)
    input_boxes.append(text_input)
    text_input.bind("<Button-1>", lambda event, widget=text_input: select_input(widget))

# Create the submit button
submit_button = tk.Button(left_frame, text="Submit", font=("Arial", 14), command=lambda: submit_inputs())
submit_button.grid(row=len(label_names)+1, column=1, pady=10)

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
    button = tk.Button(right_frame, text=str(i), font=("Arial", 24), command=lambda num=i: button_click(num))
    button.grid(row=(i-1)//3, column=(i-1)%3, padx=10, pady=10, sticky="nsew")

# Create a dot button
button_dot = tk.Button(right_frame, text=".", font=("Arial", 24), command=lambda: button_click("."))
button_dot.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Create a button for zero
button_zero = tk.Button(right_frame, text="0", font=("Arial", 24), command=lambda: button_click(0))
button_zero.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Create a delete button
button_delete = tk.Button(right_frame, text="←", font=("Arial", 24), command=lambda: [widget.delete(len(widget.get())-1) for widget in input_boxes if widget==selected_input])
button_delete.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# Create a button to clear all the text inputs
button_clear = tk.Button(right_frame, text="Clear", font=("Arial", 14), command=lambda: [widget.delete(0, tk.END) for widget in input_boxes])
button_clear.grid(row=4, column=1, pady=10)

def submit_inputs():
    # Get the values from the text input widgets and print them
    values = [widget.get() for widget in input_boxes]
    print(values)

root.mainloop()