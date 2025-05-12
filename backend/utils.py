# backend/utils.py
from io import BytesIO
from PIL import Image
from torchvision import transforms

MEAN = [0.485, 0.456, 0.406]
STD  = [0.229, 0.224, 0.225]

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=MEAN, std=STD),
])

def preprocess_image(image):

    if hasattr(image, "read"):
        img = Image.open(image).convert("RGB")
    else:
        img = image.convert("RGB")
    t = transform(img)
    return t.unsqueeze(0)
