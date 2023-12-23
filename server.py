# app.py
import streamlit as st
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import threading
import matplotlib.pyplot as plt
import base64
from utilities.utils import detect_objects

# Get secrets from Streamlit Secrets
secrets = st.secrets

# Get host, port, and upload folder from secrets
host = secrets['host']
port = secrets['port']
upload_folder = secrets['upload_folder']

# Create a SessionState to persist server state
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Create a SessionState to persist server state
state = SessionState(server_running=False)

def start_server():
    app = Flask(__name__)
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

            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(file_path)

            # image_file = plt.imread(file_path)
            buffer = detect_objects(file)
            face_base64 = base64.b64encode(buffer).decode('utf-8')

            st.success(f"Image '{filename}' processed and result sent.")
            return jsonify({'result_image_base64': face_base64})

    app.run(host=host, port=port)

def stop_server():
    # Access the server object and stop it
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()

# Streamlit UI
st.title('Image Upload App')
st.header("Server Logs")

if st.button("Start Server"):
    if not state.server_running:
        st.write("Starting server. Listening for incoming requests.")
        state.server_running = True

        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
    else:
        st.warning("Server is already running. Stop it first before starting again.")

if st.button("Stop Server"):
    if state.server_running:
        st.write("Stopping server.")
        state.server_running = False

        # Stop the server
        stop_server()

        st.success("Server successfully stopped.")
    else:
        st.warning("Server is not running.")
