import tkinter as tk

def calculate_speed():
    target_width = float(width_entry.get())
    bow_ibo = float(ibo_entry.get())
    draw_length = float(draw_length_entry.get())
    draw_weight = float(draw_weight_entry.get())
    additional_weight = float(additional_weight_entry.get())
    arrow_weight = float(arrow_weight_entry.get())

    speed = (bow_ibo - 5) * (draw_length / 28) - additional_weight
    speed /= (arrow_weight / 7000)
    speed += 5
    speed = round(speed, 2)

    result_label.config(text=f"The speed is: {speed} FPS")

# Create the main window
window = tk.Tk()
window.title("Archery Equipment")

# Create the labels and entry fields for each piece of information
width_label = tk.Label(window, text="Target width (inches):")
width_entry = tk.Entry(window)

ibo_label = tk.Label(window, text="Bow IBO (FPS):")
ibo_entry = tk.Entry(window)

draw_length_label = tk.Label(window, text="Draw length (inches):")
draw_length_entry = tk.Entry(window)

draw_weight_label = tk.Label(window, text="Draw weight (pounds):")
draw_weight_entry = tk.Entry(window)

additional_weight_label = tk.Label(window, text="Additional weight (grains):")
additional_weight_entry = tk.Entry(window)

arrow_weight_label = tk.Label(window, text="Arrow weight (grains):")
arrow_weight_entry = tk.Entry(window)

result_label = tk.Label(window, text="")

# Create the button to calculate the speed
calculate_button = tk.Button(window, text="Calculate speed", command=calculate_speed)

# Place the widgets in the window
width_label.grid(row=0, column=0, sticky="e")
width_entry.grid(row=0, column=1)

ibo_label.grid(row=1, column=0, sticky="e")
ibo_entry.grid(row=1, column=1)

draw_length_label.grid(row=2, column=0, sticky="e")
draw_length_entry.grid(row=2, column=1)

draw_weight_label.grid(row=3, column=0, sticky="e")
draw_weight_entry.grid(row=3, column=1)

additional_weight_label.grid(row=4, column=0, sticky="e")
additional_weight_entry.grid(row=4, column=1)

arrow_weight_label.grid(row=5, column=0, sticky="e")
arrow_weight_entry.grid(row=5, column=1)

calculate_button.grid(row=6, column=0, columnspan=2)

result_label.grid(row=7, column=0, columnspan=2)

# Run the window
window.mainloop()