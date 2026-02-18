from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import qrcode
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Configuration for upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera_view')
def camera_view():
    return render_template('camera_view.html')

@app.route('/capture_screenshot', methods=['POST'])
def capture_screenshot():
    data = request.get_json()
    img_data = data['image'] # Base64 encoded image
    camer-id = data['camera'] # Corrected typo
    
    # Decode base64 image
    header, encoded = img_data.split(",", 1)
    binary_data = base64.b64decode(encoded)

    # Save image to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{camer-id}_{timestamp}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        with open(filepath, "wb") as fh:
            fh.write(binary_data)
        print(f"Screenshot saved to {filepath}")
        return jsonify({'status': 'success', 'message': f'Screenshot from {camer-id} saved to {filepath}.'})
    except Exception as e:
        print(f"Error saving screenshot: {e}")
        return jsonify({'status': 'error', 'message': f'Error saving screenshot: {e}'}), 500


@app.route('/upload_recording', methods=['POST'])
def upload_recording():
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'No video file provided.'}), 400

    video_file = request.files['video']
    camer-id = request.form.get('camera', 'unknown') # Corrected typo
    
    if video_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{camer-id}_{timestamp}.webm"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            video_file.save(filepath)
            print(f"Recording saved to {filepath}")
            return jsonify({'status': 'success', 'message': f'Recording from {camer-id} saved to {filepath}.'})
        except Exception as e:
            print(f"Error saving recording: {e}")
            return jsonify({'status': 'error', 'message': f'Error saving recording: {e}'}), 500
    
    return jsonify({'status': 'error', 'message': 'Failed to save recording.'}), 500


@app.route('/upload_to_onedrive', methods=['POST'])
def upload_to_onedrive():
    # This is a conceptual placeholder for OneDrive integration.
    # Real integration would involve:
    # 1. OAuth 2.0 authentication with Microsoft Graph API.
    # 2. Obtaining an access token for the user's OneDrive.
    # 3. Receiving the file (screenshot or recording) from the client.
    # 4. Using the Microsoft Graph API to upload the file to OneDrive.
    #    (e.g., PUT request to a pre-authenticated upload URL or POST for simple uploads)
    
    # For demonstration, we'll just acknowledge the request.
    print("Received request to upload to OneDrive (conceptual).")
    return jsonify({'status': 'success', 'message': 'Conceptual upload to OneDrive received.'})

@app.route('/upload_to_googledrive', methods=['POST'])
def upload_to_googledrive():
    # This is a conceptual placeholder for Google Drive integration.
    # Real integration would involve:
    # 1. OAuth 2.0 authentication with Google Drive API.
    # 2. Obtaining an access token for the user's Google Drive.
    # 3. Receiving the file (screenshot or recording) from the client.
    # 4. Using the Google Drive API to upload the file.
    #    (e.g., multipart upload for files and metadata)

    # For demonstration, we'll just acknowledge the request.
    print("Received request to upload to Google Drive (conceptual).")
    return jsonify({'status': 'success', 'message': 'Conceptual upload to Google Drive received.'})

@app.route('/upload_to_mega', methods=['POST'])
def upload_to_mega():
    # This is a conceptual placeholder for Mega.nz integration.
    # Real integration would involve:
    # 1. Using a Mega.nz API client library (e.g., `mega.py`).
    # 2. Authenticating with Mega.nz (username/password or session token).
    # 3. Receiving the file (screenshot or recording) from the client.
    # 4. Encrypting the file locally (Mega.nz uses client-side encryption).
    # 5. Uploading the encrypted file to Mega.nz.

    # For demonstration, we'll just acknowledge the request.
    print("Received request to upload to Mega.nz (conceptual).")
    return jsonify({'status': 'success', 'message': 'Conceptual upload to Mega.nz received.'})


@app.route('/generate_qr_page')
def generate_qr_page():
    data = request.args.get('data', '')
    if data:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save it to a bytes buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encode to base64
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return render_template('qr_display.html', qr_code_img=img_str)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)