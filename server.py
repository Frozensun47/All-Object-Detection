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
host = "0.0.0.0"
port = 4747
upload_folder = "server_data"

st.title('Image Upload App')

# Server Side
st.header("Server Logs")
if st.button("Start Server"):
    st.write("Server started. Listening for incoming requests.")

    def get_app():
        return Flask(__name__)

    app = get_app()
    app.config['UPLOAD_FOLDER'] = upload_folder

    @app.route('/inbound', methods=['POST'])
    def receive_image():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            filename = secure_filename(file.filename)
            # Update the placeholders
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            image_file = np.array(Image.open(file_path))
            processed_image = detect_objects(image_file)
            
            image = Image.fromarray(processed_image)
            # Encode the image to base64 without decoding it to UTF-8
            buffer = BytesIO()
            image.save(buffer, format="JPEG")  # You can change the format if your image is in a different format
            img_str = base64.b64encode(buffer.getvalue()).decode()
            # Send the processed image back to the client
            return jsonify({'image': img_str})
                

            # except Exception as e:
            #     # Handle the exception, e.g., log the error or return an error response
            #     st.error(f"Error processing image: {str(e)}")
            #     return jsonify({'error': 'Image processing failed'})

    if __name__ == '__main__':
        # Change host and port to use secrets
        app.run(host=host, port=port)
