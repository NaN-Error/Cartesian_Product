import itertools
import os
import tkinter as tk
from tkinter import filedialog
import concurrent.futures

def cartesian_product(sets):
    result = list(itertools.product(*sets))
    return result

def duplicate_set(set_to_duplicate, times):
    duplicated_set = set_to_duplicate.copy()
    for _ in range(times - 1):
        duplicated_set += set_to_duplicate
    return duplicated_set

def generate_cartesian_product(event=None):
    # Get the user input for the number of sets to combine
    try:
        duplicate_times = int(duplicate_entry.get())
        if duplicate_times < 0:
            raise ValueError
    except ValueError:
        result_label.config(text="Please enter a non-negative integer.")
        return

    # Define the sets
    set1 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    set2 = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # If duplicate_times is 0, save set1 elements only to text file
    if duplicate_times == 0:
        output_file_path = os.path.join(script_dir, "set1_elements.txt")

        with open(output_file_path, "w") as file:
            for element in set1:
                file.write(element + "\n")

        result_label.config(text="Set1 elements saved.")
        open_result_file(output_file_path)
        return

    # Generate the cartesian product
    sets_to_combine = [set1]

    for i in range(duplicate_times):
        duplicated_set2 = duplicate_set(set2, i + 1)
        sets_to_combine.append(duplicated_set2)

    # Create the output file path in the same directory as the script
    output_file_path = os.path.join(script_dir, "cartesian_output.txt")

    # Use multithreading for cartesian product generation
    with concurrent.futures.ThreadPoolExecutor() as executor:
        cartesian_result = list(executor.map(cartesian_product, [sets_to_combine]))[0]

    # Open the file for writing
    with open(output_file_path, "w") as file:
        # Write the result to the file without spaces
        for element in cartesian_result:
            file.write(''.join(element) + "\n")

    result_label.config(text="Cartesian product result saved.")
    open_result_file(output_file_path)

def open_result_file(file_path):
    os.startfile(file_path)

# Get the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the main window
window = tk.Tk()
window.title("Cartesian Product Generator")

# Calculate the desired window size as 25% of the monitor size
window_width = int(window.winfo_screenwidth() * 0.25)
window_height = int(window.winfo_screenheight() * 0.25)

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{window.winfo_screenwidth()//2 - window_width//2}+{window.winfo_screenheight()//2 - window_height//2}")

# Create a frame to hold the objects
frame = tk.Frame(window)
frame.pack(expand=True)

# Create a label and entry for the number of sets to combine
duplicate_label = tk.Label(frame, text="How many times you want to combine set 1 with set 2?")
duplicate_label.pack(anchor='center')
duplicate_entry = tk.Entry(frame)
duplicate_entry.pack(anchor='center')
duplicate_entry.focus()

# Bind the Enter key to the generate function
duplicate_entry.bind("<Return>", generate_cartesian_product)

# Create a button to generate the Cartesian product
generate_button = tk.Button(frame, text="Generate Cartesian Product", command=generate_cartesian_product)
generate_button.pack(anchor='center')

# Create a label for the result message
result_label = tk.Label(frame, text="")
result_label.pack(anchor='center')

# Start the Tkinter event loop
window.mainloop()