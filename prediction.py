import os
import cv2 as cv
import statistics
import numpy as np
from glob import glob
from pathlib import Path
from statistics import mode
# from keras.preprocessing import image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import model_from_json


class_names = {

    0: 'Arson',
    1: 'Burglary',
    2: 'Explosion',
    3: 'Fighting',
    4: 'Normal'

}

f = Path("models/model_structure.json")

model_structure = f.read_text()

model = model_from_json(model_structure)

model.load_weights("models/model_weights.h5")


def predict_label(path):
    files = glob('static/temp/*')

    for f in files:
        os.remove(f)
    predict = []
    count = 0
    cap = cv.VideoCapture(path)  # capturing the video from the given path
    while (cap.isOpened()):
        # reading from frame
        ret, frame = cap.read()
        if ret:
            if count % 300 == 0:
                filename = 'static/temp/' + "_frame%d.jpg" % count
                # writing the extracted images
                cv.imwrite(filename, frame)
            count += 1
        else:
            break
    cap.release()
    # cv.destroyAllWindows()
    images = glob("static/temp/*.jpg")
    prediction_images = []
    for i in range(len(images)):
        img = load_img(images[i], target_size=(64, 64, 3))
        img = img_to_array(img)
        img = img / 255
        prediction_images.append(img)
    prediction_images = np.array(prediction_images)
    y_pred = model.predict(prediction_images, batch_size=1, verbose=0)
    acc = max(y_pred[0]) * 100
    acc = float(f'{acc:.2f}')
    y_predict = []
    for i in range(0, len(y_pred)):
        y_predict.append(int(np.argmax(y_pred[i])))

    def most_common(List):
        return mode(List)

    l = list(y_predict)
    most_likely_class_index = most_common(l)
    class_label = class_names[most_likely_class_index]
    print('This video clasify as a ', class_label)
    print("Probability score:", acc)
    return class_label, acc


