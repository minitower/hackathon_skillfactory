from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.models import load_model
from src.autoencoder import Autoencoder
import pathlib
import pickle

class Similar():
    def __init__(self):
        '''
        Class for find similar image by K-neighbors method
        '''
        self.model_path = pathlib.Path(__file__).parent.resolve()/'models' # path to models
        self.model_path = self.model_path.resolve()
        self.load_autoencoder() # load autoencoder models in class variables
        self.autoencoder = Autoencoder()
        with open(str(self.model_path/'codes.pickle'), 'rb') as f:
            self.codes = pickle.load(f) # load codes from autoencoder
        self.k_mean = NearestNeighbors(metric="euclidean")
        self.k_mean.fit(self.codes) # fit K-neighbors class
        
    def find_img(self, image_path):
        img = self.autoencoder.preprocess_image(image=image_path) # preprocess image
        code = self.encoder.predict(img[None]) # encode image
        return self.k_mean.kneighbors(code, 1) # return 1 id from codes
        
    def load_autoencoder(self):
        self.encoder = load_model(str(self.model_path/'encoder.keras'))
        self.decoder = load_model(str(self.model_path/'decoder.keras'))
        self.autoencoder = load_model(str(self.model_path/'autoencoder.keras'))