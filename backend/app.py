from flask import Flask, request, jsonify, send_from_directory
import os
import pickle
from speech_emotion_recognition_with_librosa import extract_feature

app = Flask(__name__)

# Paths
UPLOAD_FOLDER = "/Users/graciabetty/Desktop/emotion detection from speech/backend/uploaded_audio"
FRONTEND_FOLDER = "/Users/graciabetty/Desktop/emotion detection from speech/frontend"
MODEL_FILE = "/Users/graciabetty/Desktop/emotion detection from speech/backend/modelForPrediction1.sav"

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the pre-trained model
model = pickle.load(open(MODEL_FILE, 'rb'))

# Serve the index.html file at the root URL
@app.route('/')
def index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

# Serve static files (CSS, JS) from the frontend folder
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract features and predict emotion
    features = extract_feature(filepath, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    prediction = model.predict(features)[0]

    return jsonify({"emotion": prediction}), 200

if __name__ == '__main__':
    app.run(debug=True)
