import streamlit as st
from PIL import Image
import pytesseract
import re
import datetime
import streamlit as st
from PIL import Image
import pytesseract
import re
import datetime

# ✅ Add this line to set the Tesseract executable path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("MedMate - Image Reminder Setup")

# Upload Image
uploaded_file = st.file_uploader("Upload an image of the medicine/prescription", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text using pytesseract
    extracted_text = pytesseract.image_to_string(image)
    st.subheader("Extracted Text")
    st.write(extracted_text)

    # Attempt to identify medicine name and times
    medicine_name = extracted_text.split('\n')[0]  # crude: take first line
    times = re.findall(r'\b\d{1,2}[:.]\d{2}\s?(AM|PM|am|pm)?\b', extracted_text)

    st.subheader("Detected Info")
    st.write(f"Medicine: **{medicine_name}**")
    if times:
        st.write("Suggested Reminder Times:")
        for t in times:
            st.write(f"🕒 {t}")
    else:
        st.write("No specific times found. You can manually add a reminder.")

    # Allow user to confirm or edit reminder details
    with st.form("set_reminder"):
        med_input = st.text_input("Medicine Name", value=medicine_name)
        time_input = st.time_input("Set Reminder Time", value=datetime.time(8, 0))
        submit = st.form_submit_button("Set Reminder")
        
        if submit:
            st.success(f"Reminder set for {med_input} at {time_input.strftime('%I:%M %p')} ✅")

