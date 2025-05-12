import os
from sqlite3 import Row
from sys import _current_frames
from turtle import window_width
import pandas as pd
from PIL import Image, ImageTk
from tkinter import filedialog, Toplevel, Label, Entry, Button, Frame, Scrollbar, VERTICAL, HORIZONTAL
from tkinter import ttk,  BooleanVar, Checkbutton
import json



image_refs=[]

filepath = {
    'stage': 'stage_log.json',
    'unitpath': 'unit_log.csv',
    'techpath': 'tech_log.csv',
    'itempath': 'item_log.csv',
    'scenepath': 'scenario_log.csv'
}

table_col=["ID","Title","Scenario", "Item", "Unit","Tech"]

win_width = 1200

def load_csv(filepath, index_col='ID'):
    """
    load the csv
    """
    df = pd.read_csv(filepath)
    df = df.set_index(index_col)
    return df

def load_data(filepath):
    """
    load all the csv
    """
    unit_df = load_csv(filepath['unitpath'])
    item_df = load_csv(filepath['itempath'])
    tech_df = load_csv(filepath['techpath'])
    scenario_df = load_csv(filepath['scenepath'])
    
    return unit_df, item_df, tech_df, scenario_df

def add_element(var, id_list, df, la, en, hv):
    global  hidden_var
        
    selected_index = var.current()  
    if selected_index != -1:  
        selected_text = id_list[selected_index]  
        if la =='Scenario':
            en['Scenario'] = selected_text
        elif la == 'Item':
            en['Item'][selected_text] = hv[0].get()
        elif la == 'Unit':
            en['Unit'][selected_text] = hv[1].get()
        elif la == 'Tech':
            en['Tech'].append(selected_text)
        update_entry(en)



def show_saved_list(filepath,tree):
    # Clear existing entries
    for row in tree.get_children():
        tree.delete(row)

    # Load data from CSV
    
    if os.path.exists(filepath['stage']):
        with open(filepath['stage'], "r", encoding="utf-8") as f:
            for line in f:
                log_data = json.loads(line)
                if os.path.exists(filepath['scenepath']):
                    scenario_df = pd.read_csv(filepath['scenepath'])
                    scenario_df = scenario_df.set_index('ID')
                #print(scenario_df.index,log_data['Scenario']);break
                img = Image.open(scenario_df.loc[log_data['Scenario']]['File Path'])
                img.thumbnail((50, 50))  # 調整圖像大小
                photo = ImageTk.PhotoImage(img)
                scenario_title= scenario_df.loc[log_data['Scenario']]['Title']
                items = "\n".join(f"{key}: {value}" for key, value in log_data['Item'].items())
                units = "\n".join(f"{key}: {value}" for key, value in log_data['Unit'].items())
                techs= "\n".join(log_data['Tech'])
                tree.insert("", "end", image=photo, values=(log_data['ID'], log_data['Title'],scenario_title,items,units,techs))


def log_stage_detail(log_data,tree):
    
    # Append to JSON
    with open("stage_log.json", "a") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
    show_saved_list(filepath,tree)
    log_data['ID'] = ""
    log_data['Title'] = ""
    
    log_data['Item'].clear()  # Clear the dictionary
    log_data['Unit'].clear()  # Clear the dictionary
    log_data['Tech'].clear()  # Clear the list

    update_entry(log_data)

def update_entry(entry):
    global entry_labels
    for col in ['ID','Title','Scenario']:
        entry_labels[table_col.index(col)].config(text=entry[col])
    for col in ['Item','Unit']:
        entry_labels[table_col.index(col)].config(text=",".join(entry[col].keys()))
    for col in ['Tech']:
        entry_labels[table_col.index(col)].config(text=",".join(entry[col]))

def update_name(entry, tbox, ikey):
    entry[ikey] = tbox.get()
    update_entry(entry)
    
def check_fields(form_frame, id_entry, title_entry, upload_button):
    
    if id_entry.get() and title_entry.get() and hasattr(form_frame, 'image_path'):
        upload_button.config(state='normal')
    else:
        upload_button.config(state='disabled')

def open_upload_window(root):
    global entry_labels
    entry_labels = []

    entry = {
    'ID': "",
    'Title': "",
    'Scenario': "",
    'Item': {},  # Initialize as an empty dictionary
    'Unit': {},  # Initialize as an empty dictionary
    'Tech': []   # Initialize as an empty list
    }
    unit_df, item_df, tech_df, scenario_df = load_data(filepath)

    upload_window = Toplevel(root)
    upload_window.title("Stage Creater")
    upload_window.geometry(f"{win_width}x800")  # Adjust window size as needed
    # Lift the upload window above the main window
    upload_window.lift()
    upload_window.transient(root)  # Make it a transient window of the main window

    style = ttk.Style(upload_window)
    style.configure('Treeview', rowheight=50)

    current_frame = Frame(upload_window, width=win_width, height=60)  # 設置寬度和高度
    current_frame.pack(padx=10, pady=10)

    Label(current_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    id_entry = Entry(current_frame)
    id_entry.grid(row=0, column=1, padx=10, pady=5)
    Label(current_frame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    title_entry = Entry(current_frame) 
    title_entry.grid(row=1, column=1, padx=10, pady=5)



        # Frame for the form
    form_frame = Frame(upload_window, width=win_width, height=200)
    form_frame.pack_propagate(False) 
    form_frame.pack(padx=10, pady=10)
    

    



    # Create dropdowns and labels for scenario, item, unit, and tech
    dropdowns = [
        ("Scenario", scenario_df, "Title"),
        ("Item", item_df, "Title"),
        ("Unit", unit_df, "Title"),
        ("Tech", tech_df, "Title"),
    ]
    hidden_var= [BooleanVar(), BooleanVar()]  # Variables to track checkbox states

    for i, (label_text, df, column) in enumerate(dropdowns):
        # Dropdown label
        Label(form_frame, text=label_text).grid(row=0, column=i, padx=10, pady=5)

        id_list = df.index.tolist()
        values = [f"{idx} - {df.loc[idx, column]}" for idx in df.index]

        # Dropdown menu
        var = ttk.Combobox(form_frame, values=values)
        var.grid(row=1, column=i, padx=10, pady=5)

        # Image label
        placeholder=ImageTk.PhotoImage(Image.new('RGB',(50,50),color='white'))
        image_label = Label(form_frame, image=placeholder)
        image_label.grid(row=2, column=i, padx=10, pady=5)
        image_label.image=placeholder        
    
        
        # Add checkboxes for the middle two columns
        if i == 1 or i == 2:  # Middle two columns
            
            Checkbutton(form_frame, text="Hidden", variable=hidden_var[i-1]).grid(row=3, column=i, padx=10, pady=5)

        Button(form_frame, text=f"Add {label_text}", command=lambda v=var, la=label_text, ids=id_list, df=df, en=entry, hv=hidden_var: add_element(v, ids, df, la, en,hv)).grid(row=4, column=i, padx=10, pady=5)

        def update_image(v, id_list, d,il):
            selected_index = v.current()
            if selected_index != -1:  # 確保選擇有效
                selected_id = id_list[selected_index]
                if selected_id in d.index:
                    image_path = d.loc[selected_id, 'File Path']
                    if os.path.exists(image_path):
                        img = Image.open(image_path)
                        img.thumbnail((50, 50))  # Resize the image
                        photo = ImageTk.PhotoImage(img)
                        image_refs.append(photo)  # Keep a reference to avoid garbage collection
                        il.config(image=photo)
                        il.image = photo
                    else:
                        il.config(image='', text="Image not found")
                else:
                    il.config(image='', text="Invalid:"+selected_id)


        # Bind selection event
        var.bind(
            "<<ComboboxSelected>>",
            lambda event, v=var,id_list=id_list, d=df, il=image_label: update_image(v, id_list,d, il),
        )


    
    

    #Table for current entry
    entry_frame = Frame(upload_window, width=win_width, height=60)  # 設置寬度和高度
    entry_frame.pack_propagate(False)  # 禁止自動調整大小
    entry_frame.pack(padx=10, pady=10)


    for ind,col in enumerate(table_col):
        Label(entry_frame, text=col).grid(row=0, column=ind, padx=10, pady=5)
        label = Label(entry_frame, text='')
        label.grid(row=1, column=ind, padx=10, pady=5)
        entry_labels.append(label)

    Button(entry_frame, text="Add Stage", command=lambda:log_stage_detail(entry,tree)).grid(row=0, rowspan=2, column=len(table_col), padx=10, pady=5)


    
    id_entry.bind("<KeyRelease>", lambda event: update_name(entry, id_entry, 'ID'))  # Bind the KeyRelease event to update the entry
    title_entry.bind("<KeyRelease>",lambda event:  update_name(entry, title_entry, 'Title'))  # Bind the KeyRelease event to update the entry

    # Table for saved items
    table_frame = Frame(upload_window, width=win_width)
    table_frame.pack(fill="both", expand=False)

    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_x.pack(side="bottom", fill="x")

    

    tree = ttk.Treeview(table_frame, columns=table_col, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tree.pack(fill="both", expand=True)

    

    scrollbar_y.config(command=tree.yview)
    scrollbar_x.config(command=tree.xview)

    
    tree.column("#0", width=0, stretch=False)
    tree.heading("#0", text="")  


    # Define headings
    for col in table_col:
        tree.heading(col, text=col)
    

    # Show saved items initially
    
    show_saved_list(filepath,tree)


    
    
