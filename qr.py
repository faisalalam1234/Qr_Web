import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw

# Function to generate QR code
def generate_qr(url, box_color, bg_color, style):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=6,  # Smaller box size for mobile compatibility
        border=2,    # Reduced border size for a compact QR code
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=box_color, back_color=bg_color)

    if style == "Stylish QR 1":
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        width, height = img.size
        draw.rectangle([width // 3, height // 3, 2 * width // 3, 2 * height // 3], fill=box_color)
    elif style == "Stylish QR 2":
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        width, height = img.size
        for x in range(0, width, 20):
            draw.line([(x, 0), (x, height)], fill=box_color, width=1)

    return img

# Streamlit App
st.title("QR Code Generator 📱")

# Input field for URL
url = st.text_input("Enter URL to generate QR Code", placeholder="https://example.com")

# Dropdown for QR style
style = st.selectbox(
    "Select QR Code style",
    ("Simple QR", "Stylish QR 1", "Stylish QR 2")
)

# Color pickers for box and background
box_color = st.color_picker("Pick box color", "#000000")
bg_color = st.color_picker("Pick background color", "#FFFFFF")

# Generate button
if st.button("Generate QR Code"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        qr_img = generate_qr(url, box_color, bg_color, style)

        # Convert PIL Image to BytesIO
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)  # Reset buffer position to the start
        
        # Display the QR code image
        st.image(buf, caption="Your QR Code", use_container_width=True)

        # Download button for QR code
        st.download_button(
            label="Download QR Code",
            data=buf.getvalue(),
            file_name="qr_code.png",
            mime="image/png",
        )

# Footer for mobile layout instructions
st.markdown("""
### Instructions for Mobile Users
1. Open this app on your mobile browser.
2. Enter a URL and generate your QR code.
3. Use the download button to save it or scan directly!
""")
