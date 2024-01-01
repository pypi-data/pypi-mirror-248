from PIL import Image

def resize_image(input_image_path, output_image_path):
    # Open the original image

    with Image.open(input_image_path) as img:
        original_width, original_height = img.size
        # Calculate the new size of image while maintaining aspect ratio
        aspect_ratio = original_width / original_height
        #if width is greater than height
        if aspect_ratio > 1:  
            new_width = 150
            new_height = int(150 / aspect_ratio)
        else:
            new_height = 150
            new_width = int(150 * aspect_ratio)
        # Create the new image with the new size
        new_img = Image.new("RGB", (150, 150))
        # Resize original image
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        # Paste resized image onto the center of new_img
        new_img.paste(img, ((150 - new_width) // 2, (150 - new_height) // 2))
        # Save the resized image
        new_img.save(output_image_path)