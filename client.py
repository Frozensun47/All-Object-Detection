# client.py
import streamlit as st
import requests
from PIL import Image
import io
import base64

# Get secrets from Streamlit Secrets
secrets = st.secrets

# Get server URL and port from secrets
server_url =  'http://10.12.228.206'#secrets['server_url']
server_port = 5432 #secrets['server_port']

st.title('Image Upload Client')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    st.write("")

    # Add "Send" and "Clear" buttons
    col1, col2 = st.columns(2)
    if col1.button("Send"):
        st.write("Sending image to server...")

        # Send image to server
        url = f'{server_url}:{server_port}/inbound'
        files = {'file': uploaded_file}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            st.success("Image successfully sent to server and saved.")

            # Get the base64 image from the response
            base64_image = response.json().get('result_image_base64')

            if base64_image:
                # Display the base64 image in Streamlit
                image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
                st.image(image, caption="Processed Image", use_column_width=True)

    # Loading bar for indication
    with st.spinner("Processing..."):
        import time
        time.sleep(3)  # Simulating processing time
