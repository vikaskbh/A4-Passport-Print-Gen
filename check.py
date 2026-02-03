from PIL import Image, ImageCms
import io

def check_color_profile(image_path):
    with Image.open(image_path) as img:
        # Check for raw ICC profile data
        icc = img.info.get("icc_profile")
        
        if icc:
            # Convert raw bytes to a readable profile name
            f = io.BytesIO(icc)
            profile = ImageCms.ImageCmsProfile(f)
            profile_name = ImageCms.getProfileDescription(profile)
            print(f"Profile Found: {profile_name}")
            return profile_name
        else:
            print("No ICC profile embedded. Usually defaults to sRGB.")
            return None

# Test it on your generated file
check_color_profile("a4_passport_print.jpg")