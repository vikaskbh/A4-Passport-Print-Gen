import os
import numpy as np
from PIL import Image, ImageCms

def lift_shadows(image, amount=1.2):
    """
    Lifts shadows using a gamma-style curve. 
    amount > 1.0 lifts shadows.
    """
    # Create a lookup table (LUT) to map pixel values
    # This formula pushes dark pixels up while leaving 255 (white) alone
    lut = [pow(i / 255.0, 1.0 / amount) * 255.0 for i in range(256)]
    # Apply to each RGB channel
    return image.point(lut * 3)

def generate_passport_sheet(input_path, output_path, adobe_icc_path=None, shadow_lift=1.2):
    DPI = 300
    A4_PX = (int(210 / 25.4 * DPI), int(297 / 25.4 * DPI))
    PHOTO_PX = (int(35 / 25.4 * DPI), int(45 / 25.4 * DPI))
    
    with Image.open(input_path) as img:
        icc_profile = img.info.get("icc_profile")
        
        if not icc_profile and adobe_icc_path and os.path.exists(adobe_icc_path):
            with open(adobe_icc_path, "rb") as f:
                icc_profile = f.read()

        # Aspect Ratio & Crop
        img_aspect = img.width / img.height
        target_aspect = PHOTO_PX[0] / PHOTO_PX[1]
        
        if img_aspect > target_aspect:
            new_width = int(target_aspect * img.height)
            offset = (img.width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, img.height))
        else:
            new_height = int(img.width / target_aspect)
            offset = (img.height - new_height) // 2
            img = img.crop((0, offset, img.width, offset + new_height))
            
        photo_thumb = img.resize(PHOTO_PX, Image.Resampling.LANCZOS)

        # --- SHADOW LIFT INSTEAD OF BRIGHTNESS ---
        # 1.0 is original. 1.2-1.4 is a good range for lifting darks.
        photo_thumb = lift_shadows(photo_thumb, amount=shadow_lift)

        sheet = Image.new("RGB", A4_PX, "white")
        
        cols, rows = 5, 6
        gap = 60  
        
        total_grid_w = (cols * PHOTO_PX[0]) + ((cols - 1) * gap)
        total_grid_h = (rows * PHOTO_PX[1]) + ((rows - 1) * gap)
        
        start_x = (A4_PX[0] - total_grid_w) // 2
        start_y = (A4_PX[1] - total_grid_h) // 2

        for r in range(rows):
            for c in range(cols):
                x = start_x + c * (PHOTO_PX[0] + gap)
                y = start_y + r * (PHOTO_PX[1] + gap)
                sheet.paste(photo_thumb, (x, y))

        sheet.save(
            output_path,
            format="JPEG",
            quality=100,
            subsampling=0,
            icc_profile=icc_profile,
            dpi=(DPI, DPI)
        )
    print(f"Success! Saved with {gap}px gap and shadows lifted by {shadow_lift}.")

ICC_PATH = "C:/Windows/System32/spool/drivers/color/AdobeRGB1998.icc"
generate_passport_sheet("input.jpg", "a4_passport_print.jpg", ICC_PATH, shadow_lift=1.4)