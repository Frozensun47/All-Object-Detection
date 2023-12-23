# client.py
import streamlit as st
import requests
from PIL import Image
import io
import base64

st.title('Image Upload Client')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    st.write("")

    # Add a "Send" button
    if st.button("Send"):
        st.write("Sending image to server...")
        
        # Send image to server
        url = 'http://10.12.173.109:5432/inbound'
        files = {'file': uploaded_file}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            st.success("Image successfully sent to server and saved.")
            
            # Get the base64 image from the response
            base64_image = response.json()['result_image_base64']
            
            # Display the base64 image in Streamlit
            image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
            st.image(image, caption="Processed Image", use_column_width=True)
            
        else:
            st.error(f"Error sending image to server. Status code: {response.status_code}")
