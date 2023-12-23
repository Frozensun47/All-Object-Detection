import cv2
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests
import numpy as np
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    
def detect_objects(image, threshold=0.9):

    temp_image = image.copy()
    inputs = processor(images=temp_image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.shape[:-1]])
    
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        label_text = model.config.id2label[label.item()]
        confidence = round(score.item(), 3)
        # print(
        #     f"Detected {label_text} with confidence "
        #     f"{confidence} at location {box}"
        # )
        
        # Draw bounding box on the image
        x, y, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 5)

        # Print the label text below the bounding box
        cv2.putText(image, label_text+" "+str(confidence), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5, cv2.LINE_AA)

        
    return image
