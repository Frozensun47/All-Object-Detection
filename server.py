# app.py
import json
import streamlit as st
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
from utilities.utils import detect_objects
from io import BytesIO
import base64
import numpy as np
from PIL import Image

# Get secrets from Streamlit Secrets
secrets = st.secrets

# Get host, port, and upload folder from secrets
host = st.secrets['host']
port = st.secrets['port']
upload_folder = st.secrets['upload_folder']

# Streamlit app title with styling
st.title('🔍 Object Detection Server')
st.markdown(
    """
    *An interactive server for object detection powered by DETR (DEtection Transfomer).*  
    """
)

# Additional Details with styling
st.write(
    """
    This server uses a Flask backend to perform object detection using a PyTorch transformer model, specifically the DETR (DEtection Transfomer).
    
    The model is trained on the COCO dataset and is capable of detecting various objects in images.
    
    To use this service, upload an image by clicking [here](https://detectobjects.streamlit.app/), and the server will provide the detected objects in the uploaded image.
    """
)

# Button to start the server with styling
if st.button("🚀 Start Server"):
    st.success("Server started. Listening for incoming requests.")

    # Flask app initialization
    def get_app():
        return Flask(__name__)

    app = get_app()
    app.config['UPLOAD_FOLDER'] = upload_folder

    # Flask route to handle incoming image uploads
    @app.route('/inbound', methods=['POST'])
    def receive_image():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            # Securely save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read the uploaded image and process it using detect_objects function
            image_file = np.array(Image.open(file_path))
            processed_image = detect_objects(image_file)

            # Convert processed image to PIL Image
            image = Image.fromarray(processed_image)

            # Encode the processed image to base64
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            # Send the processed image back to the client
            return jsonify({'image': img_str})

    if __name__ == '__main__':
        # Run the Flask app with specified host and port
        app.run(host=host, port=port)

image_url = 'https://media.licdn.com/dms/image/D4D03AQEMw8cjnd7zbQ/profile-displayphoto-shrink_400_400/0/1698397499956?e=1709164800&v=beta&t=0sbwPaWNNHLf2TyPrQVbe8KzMLBiqsqFLQ-USqL0ocs'

# Display the image beside your name
st.image(image_url, caption='Your LinkedIn Profile Picture', width=100)
# Footer with styling
st.markdown(
    """
    ***
    ### About the Author
    **Name:** Sagar Srivastava  
    **Affiliation:** IIT BHU Varanasi  
    **Links:** [GitHub](https://github.com/Frozensun47) | [Portfolio](https://sites.google.com/itbhu.ac.in/sagarsrivastava/about) | [Medium](https://sagar-srivastava.medium.com/) | [Kaggle](https://www.kaggle.com/sagarsrivastava24/competitions) | [Twitter](https://twitter.com/Frozensun47)
    """
)
