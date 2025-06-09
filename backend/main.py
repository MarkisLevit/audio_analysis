from flask import jsonify, request
from config import app, db
from models import Audio
import os
import numpy as np
from utils import analyze_audio_file, find_similar_tracks, features_to_vector
from flask import render_template

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

# Функція аналізу аудіо
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files["file"]
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    features = analyze_audio_file(file_path)
    vector = features_to_vector(features)

     # Зберігаємо у БД
    new_track = Audio(title=file.filename, vector=vector, features=features)
    db.session.add(new_track)
    db.session.commit()

    return jsonify({"message": "Аналіз завершено", "features": features})

# Пошук схожих
@app.route("/similar", methods=["POST"])
def similar():
    data = request.get_json()
    print("DATA:", data)
    print("FEATURES:", data["features"])
    input_features = np.array(data["features"])
    print("NP ARRAY:", input_features, input_features.shape)
    similar_tracks = find_similar_tracks(input_features)
    return jsonify(similar_tracks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

