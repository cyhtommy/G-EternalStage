from PIL import Image
import os

def batch_crop_images(input_folder, output_folder, crop_coordinates):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.PNG')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Crop the image
                cropped_img = img.crop(crop_coordinates)
                # Save the cropped image
                cropped_img.save(os.path.join(output_folder, filename))
                print(f"Cropped and saved: {filename}")

if __name__ == "__main__":
    # Define your crop coordinates (left, upper, right, lower)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    crop_coords = (333, 457, 518, 642)  # Change this to your needs

    # Define input and output folders
    input_folder = 'image/unit/raw'
    output_folder = 'image/unit'

    batch_crop_images(input_folder, output_folder, crop_coords)




