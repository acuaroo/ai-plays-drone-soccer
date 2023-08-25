import numpy as np

from controller import log


class Model:
    def __init__(self, model_path, verbose=False):
        super().__init__()

        self.model_path = model_path
        self.verbose = verbose

        # TEMP
        self.model = None
        self.detokenizer = None

        # TODO: load the model & the detokenizer

    def infer(self, image):
        image = np.expand_dims(image, axis=0)

        predictions = self.model.predict(image)[0]
        predictions = np.argmax(predictions)

        result = self.detokenizer[predictions]

        if self.verbose:
            log(f"model inferred: {result}", "normal")

        return result
