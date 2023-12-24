import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from base64 import b64decode

# Set Streamlit title
st.title('Object Detection Client')

# Description of the App
st.markdown(
    """
    This Streamlit app allows you to upload an image and send it to the Object Detection Server. 
    Once processed, the server returns the image with detected objects highlighted.
    """
)
image_url = 'https://media.licdn.com/dms/image/D4D03AQEMw8cjnd7zbQ/profile-displayphoto-shrink_400_400/0/1698397499956?e=1709164800&v=beta&t=0sbwPaWNNHLf2TyPrQVbe8KzMLBiqsqFLQ-USqL0ocs'
# Author Information
st.sidebar.title('About the Author')
st.sidebar.image(image_url, width=100)
st.sidebar.markdown(
    """
        **Name:** Sagar Srivastava  
        **Affiliation:** IIT BHU Varanasi  
        **Links:** [GitHub](https://github.com/Frozensun47) | [Portfolio](https://sites.google.com/itbhu.ac.in/sagarsrivastava/about) | [Medium](https://sagar-srivastava.medium.com/) | [Kaggle](https://www.kaggle.com/sagarsrivastava24/competitions) | [Twitter](https://twitter.com/Frozensun47)
    """
)
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
        result_placeholder.write("Sending image to the server...")

        # Retrieve the server URL from Streamlit Secrets
        server_url = 'http://10.12.226.61:4747' #f'{st.secrets["url"]}:{st.secrets["port"]}'

        # Send the image to the server
        files = {'file': uploaded_file}
        response = requests.post(server_url + '/inbound', files=files, stream=True)

        if response.status_code == 200:
            # Display the processed image received from the server
            try:
                result_placeholder.success("Processed Image received from the server")
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
