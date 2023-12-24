# client.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from base64 import b64decode
st.title('Image Upload Client')
save_path = 'client_data/image.jpg'
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    # Add a "Send" button
    if st.button("Send"):
        result_placeholder = st.empty()
        result_placeholder.write("Sending image to server...")
        # Send image to server
        url = 'http://192.168.0.106:4747/inbound'
        files = {'file': uploaded_file}
        response = requests.post(url, files=files, stream=True)
        if response.status_code == 200:
            # Display the processed image received from the server
            try:
                result_placeholder.success("Processed Image received from server")
                img_object = Image.open(BytesIO(b64decode(response.json()['image'])))
                st.image(img_object, caption="Processed Image", use_column_width=True)
                # # Optionally, save the processed image locally
                # img_object.save(save_path)
                # print(f"Processed Image saved to {save_path}")
            except:
                try:
                    result_placeholder.error(response.json()['error'])
                except:
                    result_placeholder.error('Client side error')
        else:
            print(f"Error: {response.status_code} - {response.text}")
