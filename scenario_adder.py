<<<<<<< HEAD
﻿import os
from sqlite3 import Row
import pandas as pd
from PIL import Image, ImageTk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL,IntVar, Checkbutton
from tkinter import ttk

image_refs=[]
csv_name='scenario_log.csv'


def show_saved_list(tree):
    # Clear existing entries
    for row in tree.get_children():
        tree.delete(row)

    # Load data from CSV
    
    if os.path.exists(csv_name):
        df = pd.read_csv(csv_name)
        for index, row in df.iterrows():
            img = Image.open(row['File Path'])
            img.thumbnail((50, 50))  
            photo = ImageTk.PhotoImage(img)
            image_refs.append(photo)  # Keep a reference
            active_symbol = "✔️" if row['Active'] else "❌"
            tree.insert("", "end", image=photo, values=(row['ID'], row['Title'],active_symbol))

def save_image(file_path, title, img_id,active_bool):
    subfolder = 'image\\scenario'
    os.makedirs(subfolder, exist_ok=True)
    
    # Save the image
    image = Image.open(file_path)
    image_name = os.path.basename(file_path)
    save_path = os.path.join(subfolder, img_id)+'.png'
    image.save(save_path)
    # Log details to CSV
    log_image_details(img_id, title, save_path,active_bool)

def log_image_details(img_id, title, file_path, active_bool):
    log_data = {'ID': [img_id], 'Title': [title], 'File Path': [file_path], 'Active': [active_bool]}
    df = pd.DataFrame(log_data)
    
    # Append to CSV
    df.to_csv(csv_name, mode='a', header=not os.path.exists(csv_name), index=False)

def upload_image(form_frame, img_id, title, image_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the selected image
        image = Image.open(file_path)
        image.thumbnail((100, 100))  # Create a thumbnail
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference
        form_frame.image_path = file_path  # Store the selected path


def check_fields(form_frame, id_entry, title_entry, upload_button):
    
    if id_entry.get() and title_entry.get() and hasattr(form_frame, 'image_path'):
        upload_button.config(state='normal')
    else:
        upload_button.config(state='disabled')

def open_upload_window(root):
    upload_window = Toplevel(root)
    upload_window.title("Image Uploader")
    upload_window.geometry("800x800")  # Adjust window size as needed
    # Lift the upload window above the main window
    upload_window.lift()
    upload_window.transient(root)  # Make it a transient window of the main window

    style = ttk.Style(upload_window)
    style.configure('Treeview', rowheight=50)

        # Frame for the form
    form_frame = Frame(upload_window)
    form_frame.pack(pady=10)

    Label(form_frame, text="ID:").pack(side="left")
    id_entry = Entry(form_frame)
    id_entry.pack(side="left", padx=5)
    id_entry.bind("<KeyRelease>", lambda e: check_fields(form_frame, id_entry, title_entry, upload_button))

    Label(form_frame, text="Title:").pack(side="left")
    title_entry = Entry(form_frame)
    title_entry.pack(side="left",padx=5)
    title_entry.bind("<KeyRelease>", lambda e: check_fields(form_frame, id_entry, title_entry, upload_button))

    Label(form_frame, text="Image:").pack(side="left")

    placeholder=ImageTk.PhotoImage(Image.new('RGB',(100,100),color='white'))
    image_label = Label(form_frame, image=placeholder)
    image_label.pack(side="left",padx=5)
    image_label.image=placeholder


    Button(form_frame, text="Browse", command=lambda: [upload_image(form_frame, id_entry.get(), title_entry.get(), image_label), check_fields(form_frame,id_entry, title_entry, upload_button)]).pack(side="left", padx=5)

    # Step 1: Create the IntVar
    active_var = IntVar()

    # Step 2: Create the checkbox
    checkbox = Checkbutton(form_frame, text="Active", variable=active_var)
    checkbox.pack(side="left", padx=5)

    # Step 3: Use active_var.get() to control active_bool
    active_bool = bool(active_var.get())

    upload_button = Button(form_frame, text="Upload", command=lambda: save(upload_window, id_entry.get(), title_entry.get(), form_frame.image_path,bool(active_var.get()),tree), state='disabled')
    upload_button.pack(side="left", padx=5)

    # Table for saved items
    table_frame = Frame(upload_window)
    table_frame.pack(fill="both", expand=True)

    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(table_frame, columns=("ID", "Title","Active"), yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(fill="both", expand=True)

    

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    # Define headings
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Active", text="Active")
    

    # Show saved items initially
    show_saved_list(tree)


    # Check fields initially
    check_fields(form_frame,id_entry, title_entry, upload_button)

def save(upload_window, img_id, title, file_path,active_bool,tree):
    if file_path:
        save_image(file_path, title, img_id, active_bool)
=======
﻿import os
from sqlite3 import Row
import pandas as pd
from PIL import Image, ImageTk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL,IntVar, Checkbutton
from tkinter import ttk

image_refs=[]
csv_name='scenario_log.csv'


def show_saved_list(tree):
    # Clear existing entries
    for row in tree.get_children():
        tree.delete(row)

    # Load data from CSV
    
    if os.path.exists(csv_name):
        df = pd.read_csv(csv_name)
        for index, row in df.iterrows():
            img = Image.open(row['File Path'])
            img.thumbnail((50, 50))  
            photo = ImageTk.PhotoImage(img)
            image_refs.append(photo)  # Keep a reference
            active_symbol = "✔️" if row['Active'] else "❌"
            tree.insert("", "end", image=photo, values=(row['ID'], row['Title'],active_symbol))

def save_image(file_path, title, img_id,active_bool):
    subfolder = 'image\\scenario'
    os.makedirs(subfolder, exist_ok=True)
    
    # Save the image
    image = Image.open(file_path)
    image_name = os.path.basename(file_path)
    save_path = os.path.join(subfolder, img_id)+'.png'
    image.save(save_path)
    # Log details to CSV
    log_image_details(img_id, title, save_path,active_bool)

def log_image_details(img_id, title, file_path, active_bool):
    log_data = {'ID': [img_id], 'Title': [title], 'File Path': [file_path], 'Active': [active_bool]}
    df = pd.DataFrame(log_data)
    
    # Append to CSV
    df.to_csv(csv_name, mode='a', header=not os.path.exists(csv_name), index=False)

def upload_image(form_frame, img_id, title, image_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the selected image
        image = Image.open(file_path)
        image.thumbnail((100, 100))  # Create a thumbnail
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference
        form_frame.image_path = file_path  # Store the selected path


def check_fields(form_frame, id_entry, title_entry, upload_button):
    
    if id_entry.get() and title_entry.get() and hasattr(form_frame, 'image_path'):
        upload_button.config(state='normal')
    else:
        upload_button.config(state='disabled')

def open_upload_window(root):
    upload_window = Toplevel(root)
    upload_window.title("Image Uploader")
    upload_window.geometry("800x800")  # Adjust window size as needed
    # Lift the upload window above the main window
    upload_window.lift()
    upload_window.transient(root)  # Make it a transient window of the main window

    style = ttk.Style(upload_window)
    style.configure('Treeview', rowheight=50)

        # Frame for the form
    form_frame = Frame(upload_window)
    form_frame.pack(pady=10)

    Label(form_frame, text="ID:").pack(side="left")
    id_entry = Entry(form_frame)
    id_entry.pack(side="left", padx=5)
    id_entry.bind("<KeyRelease>", lambda e: check_fields(form_frame, id_entry, title_entry, upload_button))

    Label(form_frame, text="Title:").pack(side="left")
    title_entry = Entry(form_frame)
    title_entry.pack(side="left",padx=5)
    title_entry.bind("<KeyRelease>", lambda e: check_fields(form_frame, id_entry, title_entry, upload_button))

    Label(form_frame, text="Image:").pack(side="left")

    placeholder=ImageTk.PhotoImage(Image.new('RGB',(100,100),color='white'))
    image_label = Label(form_frame, image=placeholder)
    image_label.pack(side="left",padx=5)
    image_label.image=placeholder


    Button(form_frame, text="Browse", command=lambda: [upload_image(form_frame, id_entry.get(), title_entry.get(), image_label), check_fields(form_frame,id_entry, title_entry, upload_button)]).pack(side="left", padx=5)

    # Step 1: Create the IntVar
    active_var = IntVar()

    # Step 2: Create the checkbox
    checkbox = Checkbutton(form_frame, text="Active", variable=active_var)
    checkbox.pack(side="left", padx=5)

    # Step 3: Use active_var.get() to control active_bool
    active_bool = bool(active_var.get())

    upload_button = Button(form_frame, text="Upload", command=lambda: save(upload_window, id_entry.get(), title_entry.get(), form_frame.image_path,bool(active_var.get()),tree), state='disabled')
    upload_button.pack(side="left", padx=5)

    # Table for saved items
    table_frame = Frame(upload_window)
    table_frame.pack(fill="both", expand=True)

    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(table_frame, columns=("ID", "Title","Active"), yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(fill="both", expand=True)

    

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    # Define headings
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Active", text="Active")
    

    # Show saved items initially
    show_saved_list(tree)


    # Check fields initially
    check_fields(form_frame,id_entry, title_entry, upload_button)

def save(upload_window, img_id, title, file_path,active_bool,tree):
    if file_path:
        save_image(file_path, title, img_id, active_bool)
>>>>>>> c179494010e219a542fad61ecf25fd9f39d8791e
        show_saved_list(tree)