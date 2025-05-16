import os
import pandas as pd
import shutil



def copy_and_rename_file(source_path, destination_path):
    # Copy the file to the destination
    
    
    shutil.copy(source_path, destination_path)
    print(f"Copied and renamed to: {destination_path}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

csv_name='unit_log.csv'

if os.path.exists(csv_name):
    df = pd.read_csv(csv_name)
    df_copy = df.copy()
    for index, row in df.iterrows():
        img_id=row['ID']
        title=row['Title']
        filepath=row['File Path']
        directory = os.path.dirname(filepath)
        destination_path = os.path.join(directory, img_id)+'.webp'
        copy_and_rename_file(filepath,destination_path)
        
        df_copy.loc[index, 'File Path'] =destination_path
    df_copy.to_csv('output_file.csv', index=False)






