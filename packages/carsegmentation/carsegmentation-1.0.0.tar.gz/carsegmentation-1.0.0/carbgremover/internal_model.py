from tensorflow import image as tf_image
from tensorflow import data as tf_data
from tensorflow import io as tf_io
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
import keras
import os

def read_image(image_path, mask=False):
    image = tf.io.read_file(image_path)
    if mask:
        image = tf.io.decode_jpeg(image, channels=1)
        image.set_shape([None, None, 1])
        image = tf.image.resize(images=image, size=[512, 512])
    else:
        image = tf.io.decode_jpeg(image, channels=3)
        image.set_shape([None, None, 3])
        image = tf.image.resize(images=image, size=[512, 512])
    return image


def infer(model, image_tensor):
    predictions = model.predict(np.expand_dims((image_tensor), axis=0))
    predictions = np.squeeze(predictions)
    predictions = (predictions > 0.5).astype(np.uint8)
    return predictions


def remove_background_internal(image_path):
    model = load_model(r'./carbgremover/pretrained_models/best_model_weights.h5')
    image_tensor = read_image(image_path)
    prediction_mask = infer(image_tensor=image_tensor, model=model)

    # Convert EagerTensor to NumPy array
    image_tensor_np = np.array(image_tensor)

    # Create a copy of the original image to modify
    result_image = np.copy(image_tensor_np)

    # Copy the car from the original image to the result image using the refined mask
    result_image[:, :, :3][prediction_mask == 1] = 255

    # Convert the modified NumPy array back to EagerTensor
    result_image = tf.convert_to_tensor(result_image)
    return result_image


def plot_image(image, figsize=(5, 3)):
    if image.shape[-1] == 3:
        plt.imshow(keras.utils.array_to_img(image))
    else:
        plt.imshow(image)
    plt.show()



