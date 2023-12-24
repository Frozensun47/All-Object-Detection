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

# Streamlit app title
st.title('Image Upload App')

# Streamlit header for server logs
st.header("Server Logs")

# Button to start the server
if st.button("Start Server"):
    st.write("Server started. Listening for incoming requests.")

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
