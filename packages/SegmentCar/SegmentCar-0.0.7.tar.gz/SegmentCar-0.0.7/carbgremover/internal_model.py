from tensorflow import image as tf_image
from tensorflow import data as tf_data
from tensorflow import io as tf_io
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
import keras
import os
import cv2
import os
import requests
from tqdm import tqdm

import torch
from torchvision import models


def loadModel(url):
    model = models.resnet18(pretrained=False)
    state_dict = torch.hub.load_state_dict_from_url(url, map_location='cpu')
    model.load_state_dict(state_dict)
    save_file_path = os.path.join('./')
    torch.save(model.state_dict(),save_file_path)
    return save_file_path

# def download_model_checkpoint():
#     checkpoint_path = "./SegmentCar-0.0.4/carbgremover/pretrained_models/best_model_weights.h5"
#
#     url = "https://huggingface.co/Nechba/car-segmentation-intern/resolve/main/best_model_weights.h5"
#     response = requests.get(url, stream=True)
#     total_size = int(response.headers.get('content-length', 0))
#     block_size = 1024  # 1 Kibibyte
#
#     progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
#
#     with open(checkpoint_path, 'wb') as file:
#         for data in response.iter_content(block_size):
#             progress_bar.update(len(data))
#             file.write(data)
#
#     progress_bar.close()

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
    modelURL = "https://huggingface.co/Nechba/car-segmentation-intern/resolve/main/best_model_weights.h5"
    save_path = loadModel(modelURL)
    model = load_model(save_path)
    image_tensor = read_image(image_path)
    prediction_mask = infer(image_tensor=image_tensor, model=model)

    # Convert EagerTensor to NumPy array
    image_tensor_np = np.array(image_tensor)

    # Create a copy of the original image to modify
    result_image = np.copy(image_tensor_np)

    # Copy the car from the original image to the result image using the refined mask
    result_image[:, :, :3][prediction_mask == 1] = 255

    return result_image


def plot_image(image, figsize=(5, 3)):
    if image.shape[-1] == 3:
        plt.imshow(keras.utils.array_to_img(image))
    else:
        plt.imshow(image)
    plt.show()



