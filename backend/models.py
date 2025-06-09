from config import db

class Audio(db.Model): # Define the Audio model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    features = db.Column(db.PickleType, nullable=False)
    vector = db.Column(db.PickleType, nullable=False)  # Vector representation of audio features
    
    '''genre_id = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # Duration in seconds
    tempo = db.Column(db.Integer, nullable=True)  # Tempo in BPM
    key = db.Column(db.String(10), nullable=True)  # Musical key
    mfcc_vector = db.Column(db.PickleType, nullable=True)  # MFCC vector for audio analysis
    zcr = db.Column(db.Float)
    centroid = db.Column(db.Float)
    chroma = db.Column(db.PickleType)  # або JSON
    def __init__(self, title, genre_id, duration, tempo=None, key=None, mfcc_vector=None):
        self.title = title
        self.genre_id = genre_id
        self.duration = duration
        self.tempo = tempo
        self.key = key
        self.mfcc_vector = mfcc_vector
'''

    def to_json(self):
        return {
            "id":self.id,
            "title":self.title,
            "genreID":self.genre_id,
            "duration":self.duration,
            "tempo":self.tempo,
            "key":self.key,
            "mfcc_vector":self.mfcc_vector   
        }