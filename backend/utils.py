import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import json
from models import Audio
from scipy.spatial.distance import cosine
from config import db
import os
import uuid

def analyze_audio_file(filepath, save_features_path=None, plot=False, plot_dir=None):
    
    if plot_dir is None:
        plot_dir = os.path.abspath(os.path.join('..', 'static', 'plots'))
    os.makedirs(plot_dir, exist_ok=True)
    uid = str(uuid.uuid4())

    """
    Аналізує аудіофайл та повертає основні ознаки.
    :param filepath: шлях до аудіофайлу
    :param save_features_path: шлях для збереження JSON з ознаками (або None)
    :param plot: чи будувати графіки (True/False)
    :return: dict з ознаками
    """
    y, sr = librosa.load(filepath, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)

    # Зберігаємо графік MFCC
    mfcc_path = f"{plot_dir}/mfcc_{uid}.png"
    plt.figure(figsize=(8, 3))
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.savefig(mfcc_path)
    plt.close()

    # Зберігаємо графік спектрального центроїда
    centroid_path = f"{plot_dir}/centroid_{uid}.png"
    plt.figure(figsize=(8, 3))
    plt.semilogy(centroid.T, label='Spectral centroid')
    plt.ylabel('Hz')
    plt.xticks([])
    plt.xlim([0, centroid.shape[-1]])
    plt.legend()
    plt.title('Spectral Centroid')
    plt.tight_layout()
    plt.savefig(centroid_path)
    plt.close()

    # Зберігаємо графік Zero-Crossing Rate
    zcr_path = f"{plot_dir}/zcr_{uid}.png"
    plt.figure(figsize=(8, 3))
    plt.plot(zcr[0])
    plt.title('Zero-Crossing Rate')
    plt.tight_layout()
    plt.savefig(zcr_path)
    plt.close()

    zcr_filename = f"zcr_{uid}.png"
    zcr_path = os.path.join(plot_dir, zcr_filename)
    mfcc_filename = f"mfcc_{uid}.png"
    mfcc_path = os.path.join(plot_dir, mfcc_filename)
    centroid_filename = f"centroid_{uid}.png"
    centroid_path = os.path.join(plot_dir, centroid_filename)

    features = {
        'tempo': float(tempo),
        'mfcc': mfccs.mean(axis=1).tolist(),
        'chroma': chroma.mean(axis=1).tolist(),
        'spectral_centroid': float(centroid.mean()),
        'zero_crossing_rate': float(zcr.mean()),
        'plots': {
            'mfcc': f"/static/plots/{mfcc_filename}",
            'centroid': f"/static/plots/{centroid_filename}",
            'zcr': f"/static/plots/{zcr_filename}"
        }
    }     

    if save_features_path:
        with open(save_features_path, 'w') as f:
            json.dump(features, f)

    return features

def features_to_vector(features):
    vec = []
    vec.append(float(features['tempo']))
    vec.append(float(features['zero_crossing_rate']))
    vec.append(float(features['spectral_centroid']))
    vec.extend(features['mfcc'])    # вже 1D масив
    vec.extend(features['chroma'])  # вже 1D масив
    return vec

def find_similar_tracks(input_vector, top_k=5):
    all_tracks = Audio.query.all()
    similarities = []

    for track in all_tracks:
        db_vector = track.vector  # dict
        dist = cosine(input_vector, db_vector)
        similarities.append({"title": track.title, "distance": round(dist, 4)})

    similarities.sort(key=lambda x: x["distance"])  # Сортуємо за зростанням подібності
    return similarities[:top_k] 