# app.py
import streamlit as st
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
import base64
from net.face import detect_objects

# Get secrets from Streamlit Secrets
secrets = st.secrets

# Get host, port, and upload folder from secrets
host = secrets['host']
port = secrets['port']
upload_folder = secrets['upload_folder']

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
            st.write(f"File '{filename}' received and saved.")
            st.info(f"Processing image: {filename}")

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            image_file = plt.imread(file_path)
            buffer = detect_objects(image_file)
            face_base64 = base64.b64encode(buffer).decode('utf-8')

            st.success(f"Image '{filename}' processed and result sent.")
            return jsonify({'result_image_base64': face_base64})

    if __name__ == '__main__':
        # Change host and port to use secrets
        app.run(host=host, port=port)
