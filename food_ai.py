# food_ai.py
import tensorflow as tf
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

model = resnet50.ResNet50(weights='imagenet')

def predict_food(img_file):
    img = Image.open(img_file).resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = resnet50.preprocess_input(x)
    preds = model.predict(x)
    decoded = resnet50.decode_predictions(preds, top=3)[0]
    return [(label, prob) for (_, label, prob) in decoded]