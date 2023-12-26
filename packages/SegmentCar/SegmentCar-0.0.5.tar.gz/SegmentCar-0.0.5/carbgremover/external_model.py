import numpy as np
import cv2
from ultralytics import YOLO
import sys
from segment_anything import sam_model_registry, SamPredictor
import keras
from matplotlib import pyplot as plt
import os
import tensorflow as tf
import os
import requests
from tqdm import tqdm
import torch
from torchvision import models

def loadModel(url):
    tf.keras.backend.clear_session()
    model = tf.saved_model.load()
    model = models.resnet18(pretrained=False)
    state_dict = torch.hub.load_state_dict_from_url(url, map_location='cpu')
    model.load_state_dict(state_dict)

    torch.save(model.state_dict(),'./')



#
#
# def load_pytorch_model(url, save_path=):
#     print("Loading PyTorch Model")
#     try:
#         # Download the model from the URL
#         model = models.resnet18(pretrained=False)
#         state_dict = torch.hub.load_state_dict_from_url(url, map_location='cpu')
#         model.load_state_dict(state_dict)
#
#         print("PyTorch Model loaded successfully...")
#
#         return model
#     except Exception as e:
#         print("Error loading PyTorch model from URL:", str(e))
#         return None


# def download_model_checkpoint():
#     checkpoint_path = "./SegmentCar-0.0.4/carbgremover/pretrained_models/sam_vit_h_4b8939.pth"
#
#     url = "https://huggingface.co/spaces/abhishek/StableSAM/resolve/main/sam_vit_h_4b8939.pth"
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


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def plot_image(image, figsize=(5, 3)):
    if image.shape[-1] == 3:
        plt.imshow(keras.utils.array_to_img(image))
    else:
        plt.imshow(image)
    plt.show()


def SegmentCar(objects, image,device):
    for results in objects:
        boxes = results.boxes
        classe = boxes.cls
        if len(classe) == 0:
            print('No car detected')
            break
        classe_names = ["person", "bicycle", "car"]
        output_index = int(classe[0])
        classe_name = classe_names[output_index]

        if len(classe) > 0 and classe[0] == 2:
            xyxy = boxes.xyxy
            x1, y1, x2, y2 = xyxy[0]
            modelURL = "https://huggingface.co/spaces/abhishek/StableSAM/blob/main/sam_vit_h_4b8939.pth"
            loadModel(modelURL)
            sam_checkpoint = r'./sam_vit_h_4b8939.pth'
            model_type = "vit_h"



            sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            sam.to(device=device)

            predictor = SamPredictor(sam)

            predictor.set_image(image)

            input_box = np.array(xyxy[0].tolist())
            masks, _, _ = predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_box[None, :],
                multimask_output=False,
            )
    mask = masks[0]

    negative_img0 = np.tile(mask[:, :, np.newaxis], (1, 1, 3)).astype(int)
    negative_img = negative_img0 * 255
    positive_img0 = np.logical_not(negative_img)
    positive_img0 = positive_img0.astype(int)
    # positive_img = positive_img0.astype(np.uint8)*255

    image[positive_img0.all(axis=2)] = [255, 255, 255]

    return image


def remove_background_external(image_path,device="cpu"):
    model = YOLO('yolov8n.pt')

    image = cv2.imread(image_path)

    objects = model(image, save=True, classes=[2])

    image_seg = SegmentCar(objects, image,device)
    return image_seg


