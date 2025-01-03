import os
import tensorflow as tf
from tensorflow.keras.models import save_model
import tensorflow.keras.layers as L
import numpy as np
import cv2
import pathlib
import pickle


class Autoencoder:
    def __init__(self):
        '''
        Main class to make vectors from image in autoencoder way
        '''
        self.img_path = pathlib.Path(__file__).parent.resolve()/'..'/'data'/'crops'
        self.model_path = pathlib.Path(__file__).parent.resolve()/'models'
        self.model_path = self.model_path.resolve()
        self.img_path = self.img_path.resolve()
        self.IMG_SHAPE = (224, 224, 3)
        self.files_arr = []
        for root, _, files in os.walk(str(self.img_path)):
            for file in files:
                self.files_arr.append(os.path.join(root,file))
                
    def preprocess_image(self, image=None):
        '''
        Preprocess image to send it in autoencoder
        
        Args:
            image (str): image path to preprocessed image. Default None
        '''
        if not image:
            img_arr = []
            for image in self.files_arr:
                img = cv2.imread(image) # read image
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #change color scheme
                img = cv2.resize(img, (224,224)) # resize image 
                img_arr.append(img)
            img_arr = np.array(img_arr)
            img_arr = img_arr.reshape(img_arr.shape[0], self.IMG_SHAPE[0], self.IMG_SHAPE[1], self.IMG_SHAPE[2])
            img_arr = img_arr.astype('float32')
            img_arr /= 255 # normalise image
            return np.array(img_arr)
        else:
            img = cv2.imread(image) # read image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #change color scheme
            img = cv2.resize(img, (224,224))# resize image 
            img=img/255 # normalise image
            return img
    
    def build_models(self, code_size):
        '''
        Function for build autoencoder model
        
        Args:
            code_size (int): result vector of autoencoder model
        '''
        H,W,C = self.IMG_SHAPE
        # encoder
        encoder = tf.keras.models.Sequential() 
        encoder.add(L.InputLayer(self.IMG_SHAPE)) 
        encoder.add(L.Conv2D(filters=32, kernel_size=(3, 3), activation='elu', padding='same'))
        encoder.add(L.MaxPooling2D(pool_size=(2, 2)))
        encoder.add(L.Conv2D(filters=64, kernel_size=(3, 3), activation='elu', padding='same'))
        encoder.add(L.MaxPooling2D(pool_size=(2, 2)))
        encoder.add(L.Conv2D(filters=128, kernel_size=(3, 3), activation='elu', padding='same'))
        encoder.add(L.MaxPooling2D(pool_size=(2, 2)))
        encoder.add(L.Conv2D(filters=256, kernel_size=(3, 3), activation='elu', padding='same'))
        encoder.add(L.MaxPooling2D(pool_size=(2, 2)))
        encoder.add(L.Flatten())
        encoder.add(L.Dense(code_size))

        # decoder
        decoder = tf.keras.models.Sequential()
        decoder.add(L.InputLayer((code_size,)))
        decoder.add(L.Dense(14*14*256))
        decoder.add(L.Reshape((14, 14, 256)))
        decoder.add(L.Conv2DTranspose(filters=128, kernel_size=(3, 3), strides=2, activation='elu', padding='same'))
        decoder.add(L.Conv2DTranspose(filters=64, kernel_size=(3, 3), strides=2, activation='elu', padding='same'))
        decoder.add(L.Conv2DTranspose(filters=32, kernel_size=(3, 3), strides=2, activation='elu', padding='same'))
        decoder.add(L.Conv2DTranspose(filters=3, kernel_size=(3, 3), strides=2, activation=None, padding='same'))
        
        return encoder, decoder
    
    def fit_model(self):
        '''
        Function for fit autoencoder model
        '''
        encoder, decoder = self.build_models(code_size=32) # build model
        inp = L.Input(self.IMG_SHAPE)
        code = encoder(inp)
        reconstruction = decoder(code)
        train_data = self.preprocess_image()

        autoencoder = tf.keras.models.Model(inputs=inp, outputs=reconstruction) # build pipeline
        autoencoder.compile(optimizer="adamax", loss='mse')
        autoencoder.fit(x=train_data, y=train_data, epochs=5, verbose=1)
        
        codes = encoder.predict(train_data) # save autoencoder result to variable
        save_model(encoder, str(self.model_path/'encoder.keras')) # save encoder model
        save_model(decoder, str(self.model_path/'decoder.keras')) # save decoder model
        save_model(autoencoder, str(self.model_path/'autoencoder.keras')) # save pipeline model
        with open(str(self.model_path/'codes.pickle'), 'wb') as f: 
            pickle.dump(codes, f) # save codes
        return codes
    