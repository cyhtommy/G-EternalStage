from tkinter import Tk, Button
import item_adder,unit_adder, tech_adder, scenario_adder, stage_adder  # Import the image handling functions
import os

# Set up the main GUI
root = Tk()
root.title("G-Eternal Database Management")
# Set the working directory to the location of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Define the buttons
buttons = [
    ("Add Item", item_adder.open_upload_window),
    ("Add Unit", unit_adder.open_upload_window),
    ("Add Tech", tech_adder.open_upload_window),
    ("Add Scenario", scenario_adder.open_upload_window),
    ("Add Stage", stage_adder.open_upload_window),
]

# Loop through the buttons and place them in a grid
for i, (text, command) in enumerate(buttons):
    row = i % 2  # Determine the row (0 for first two buttons, 1 for next two, etc.)
    column = i // 2  # Determine the column (0 or 1)
    Button(root, text=text, command=lambda cmd=command: cmd(root)).grid(row=row, column=column, pady=20)


root.mainloop()