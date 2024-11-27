from rembg import remove
from PIL import Image
from io import BytesIO
import streamlit as st

# Handle compatibility with Pillow versions
try:
    resampling_mode = Image.Resampling.LANCZOS
except AttributeError:
    resampling_mode = Image.ANTIALIAS

def replace_background(foreground, background):
    """
    Replace the background of an image with another image.
    
    Args:
    - foreground (BytesIO): The input image with the background to be removed.
    - background (PIL.Image.Image): The new background image.
    
    Returns:
    - PIL.Image.Image: The resulting image with the replaced background.
    """
    # Remove the background
    output_image = remove(foreground)

    # Open the output image and new background with Pillow
    fg = Image.open(BytesIO(output_image))
    bg = background.resize(fg.size, resampling_mode)

    # Paste the foreground (with alpha) onto the new background
    bg.paste(fg, (0, 0), fg)
    return bg

# Streamlit App
st.title("Background Removal and Replacement App")
st.write("Upload an image to remove its background and replace it with a new background.")

# File upload widgets
foreground_file = st.file_uploader("Upload the foreground image", type=["png", "jpg", "jpeg"])
background_file = st.file_uploader("Upload the background image", type=["png", "jpg", "jpeg"])



if foreground_file and background_file:
    # Load images
    foreground_image = foreground_file.read()
    background_image = Image.open(background_file)

    # Process the images
    with st.spinner("Processing..."):
        result_image = replace_background(foreground_image, background_image)

    # Display the result
    st.success("Done!")
    st.image(result_image, caption="Resulting Image", use_container_width =True)

    # Download button
    buffer = BytesIO()
    result_image.save(buffer, format="PNG")
    buffer.seek(0)
    st.download_button(
        label="Download Result",
        data=buffer,
        file_name="output.png",
        mime="image/png"
    )

