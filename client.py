# client.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from base64 import b64decode

# Set Streamlit title
st.title('Image Upload Client')

# Define the path to save the uploaded image
save_path = 'client_data/image.jpg'

# Allow the user to upload an image
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    st.write("")

    # Add a "Send" button
    if st.button("Send"):
        # Placeholder for displaying results
        result_placeholder = st.empty()
        result_placeholder.write("Sending image to server...")

        # Retrieve the server URL from Streamlit Secrets
        server_url = f'{st.secrets["server_url"]}:{st.secrets["port"]}'

        # Send the image to the server
        files = {'file': uploaded_file}
        response = requests.post(server_url + '/inbound', files=files, stream=True)

        if response.status_code == 200:
            # Display the processed image received from the server
            try:
                result_placeholder.success("Processed Image received from server")
                img_object = Image.open(BytesIO(b64decode(response.json()['image'])))
                st.image(img_object, caption="Processed Image", use_column_width=True)
            except Exception as e:
                result_placeholder.error(f"Error displaying processed image: {str(e)}")
        else:
            # Display error information if the request was not successful
            try:
                error_message = response.json().get('error', 'Unknown error')
                result_placeholder.error(error_message)
            except:
                result_placeholder.error(f"Error: {response.status_code} - {response.text}")
