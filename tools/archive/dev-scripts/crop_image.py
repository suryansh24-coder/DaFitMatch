from PIL import Image
import sys

image_path = '/Users/shwetamgoel/.gemini/antigravity/brain/19ac18ce-8a5a-46c6-a56a-bcd9a61ee97b/.user_uploaded/media_1790957014610.png'
out_path = 'public/images/try-on/casual/casual-02.jpg'

try:
    img = Image.open(image_path)
    width, height = img.size
    
    # 5 panels, so each panel is width / 5
    panel_width = width // 5
    
    # The second panel is index 1
    # left, upper, right, lower
    # Let's crop slightly inside the divider line if possible, or just exact fifths.
    # The prompt says "Do not include... the white divider lines"
    # Let's see if we can shave off a few pixels for the divider.
    left = panel_width
    right = panel_width * 2
    
    # Let's crop exactly first, maybe shave 2 pixels off left and right to remove divider
    box = (left + 2, 0, right - 2, height)
    
    cropped_img = img.crop(box)
    
    # Convert to RGB because we are saving as JPG (which doesn't support alpha)
    if cropped_img.mode in ("RGBA", "P"):
        cropped_img = cropped_img.convert("RGB")
        
    cropped_img.save(out_path, format='JPEG', quality=95)
    
    print(f"Successfully cropped image.")
    print(f"Original size: {width}x{height}")
    print(f"Cropped size: {cropped_img.size[0]}x{cropped_img.size[1]}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
