from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.models import load_model
from src.autoencoder import Autoencoder
import pathlib
import pickle

class Similar():
    def __init__(self):
        self.model_path = pathlib.Path(__file__).parent.resolve()/'models'
        self.model_path = self.model_path.resolve()
        self.load_autoencoder()
        self.autoencoder = Autoencoder()
        with open(str(self.model_path/'codes.pickle'), 'rb') as f:
            self.codes = pickle.load(f)
        self.k_mean = NearestNeighbors(metric="euclidean")
        self.k_mean.fit(self.codes)
        
    def find_img(self, image_path):
        img = self.autoencoder.preprocess_image(image=image_path)
        code = self.encoder.predict(img[None])
        return self.k_mean.kneighbors(code, 5)
        
    def load_autoencoder(self):
        self.encoder = load_model(str(self.model_path/'encoder.keras'))
        self.decoder = load_model(str(self.model_path/'decoder.keras'))
        self.autoencoder = load_model(str(self.model_path/'autoencoder.keras'))