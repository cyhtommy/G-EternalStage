import os
from sqlite3 import Row
import pandas as pd
from PIL import Image, ImageTk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL
from tkinter import ttk

image_refs=[]
csv_name='tech_log.csv'

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
            tree.insert("", "end", image=photo, values=(row['ID'], row['Title']))

def save_image(file_path, title, img_id):
    subfolder = 'image\\tech'
    os.makedirs(subfolder, exist_ok=True)
    
    # Save the image
    image = Image.open(file_path)
    image_name = os.path.basename(file_path)
    save_path = os.path.join(subfolder, img_id)+'.png'
    image.save(save_path)
    # Log details to CSV
    log_image_details(img_id, title, save_path)

def log_image_details(img_id, title, file_path):
    log_data = {'ID': [img_id], 'Title': [title], 'File Path': [file_path]}
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


    upload_button = Button(form_frame, text="Upload", command=lambda: save(upload_window, id_entry.get(), title_entry.get(), form_frame.image_path,tree), state='disabled')
    upload_button.pack(side="left", padx=5)

    # Table for saved items
    table_frame = Frame(upload_window)
    table_frame.pack(fill="both", expand=True)

    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(table_frame, columns=("ID", "Title"), yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(fill="both", expand=True)

    

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    # Define headings
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    

    # Show saved items initially
    show_saved_list(tree)


    # Check fields initially
    check_fields(form_frame,id_entry, title_entry, upload_button)

def save(upload_window, img_id, title, file_path,tree):
    if file_path:
        save_image(file_path, title, img_id)
        show_saved_list(tree)