import numpy as np
import pickle

from controller import log

import tensorflow as tf
from tensorflow import keras
def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pickle.load(f)
    return ret_di

class Model:
    def __init__(self, model_path, verbose=False):
        super().__init__()

        self.model_path = model_path
        self.verbose = verbose

        self.model = None
        self.detokenizer = None

        # self.set_model(model_path)

    def infer(self, image):
        image = np.expand_dims(image, axis=0)

        predictions = self.model.predict(image)[0]
        predictions = np.argmax(predictions)

        result = self.detokenizer[predictions]

        if self.verbose:
            log(f"model inferred: {result}", "normal")

        return result

    def set_model(self, model_path):
        self.model = keras.load_model(f"{model_path}/model.h5")
        self.detokenizer = load_dict(f"{model_path}/detokenizer.pkl")
