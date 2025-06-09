from flask import Flask, request, render_template, jsonify
from backend.main import analyze_audio, find_similar  #  тут основна логіка

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # шаблон із templates/

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['audio']
    features, genre = analyze_audio(file)
    return jsonify({'features': features, 'genre': genre})

@app.route('/find_similar', methods=['POST'])
def similar():
    user_features = request.json['features']
    similar_tracks = find_similar(user_features)
    return jsonify(similar_tracks)

if __name__ == '__main__':
    app.run(debug=True)
