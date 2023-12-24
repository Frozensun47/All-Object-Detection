import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

def detect_objects(image, threshold=0.9):
    temp_image = image.copy()
    inputs = processor(images=temp_image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.shape[:-1]])

    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]

    # Convert the image to NumPy array for Matplotlib
    image_np = np.array(temp_image).astype(np.uint8)

    fig, ax = plt.subplots(1)
    ax.imshow(image_np)

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        label_text = model.config.id2label[label.item()]
        confidence = round(score.item(), 3)

        # Draw bounding box on the image
        x, y, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        rect = plt.Rectangle((x, y), x2 - x, y2 - y, fill=False, color='lime', linewidth=5)
        ax.add_patch(rect)

        # Print the label text below the bounding box
        text = f"{label_text} {confidence}"
        ax.text(x, y - 20, text, fontsize=12, color='lime', weight='bold')

    plt.axis("off")

    # Convert the plot to a NumPy array
    fig.canvas.draw()
    image_array = np.array(fig.canvas.renderer.buffer_rgba())

    plt.close(fig)
    image_pil = Image.fromarray(image_array)
    image_rgb = image_pil.convert('RGB')
    image_array_rgb = np.array(image_rgb)

    return image_array_rgb
