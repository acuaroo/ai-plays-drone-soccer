import numpy as np
import pickle

from controller import log

import tensorflow as tf
from tensorflow import keras

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
        self.model = tf.keras.models.load_model(f"{model_path}/model.h5")
        self.detokenizer = np.load(f"{model_path}/detokenizer.npy", allow_pickle=True).item()
