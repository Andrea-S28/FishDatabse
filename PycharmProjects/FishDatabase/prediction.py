import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Normalize, RandomHorizontalFlip, Resize, ToTensor
from PIL import Image
import os

def load_dataset():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Current Directory
    path_to_data = os.path.join(script_dir, '../FishDatabase/fish_dataset')  # Adjust Path
    if not os.path.exists(path_to_data):
        raise FileNotFoundError(f'Dataset path not found: {path_to_data}')

    return ImageFolder(path_to_data)

def get_model_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Current Directory
    path_to_model = os.path.join(script_dir, "fish_model.pth")  # Adjust Path
    # model_load_path = "./fish_model.pth"
    return path_to_model

def load_model():
    # pre-trained model for image recognition
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_load_path = get_model_path()
    model = resnet18(weights=ResNet18_Weights.DEFAULT)  # Initialize model
    model.fc = nn.Linear(in_features=512, out_features=36)  # Adjust for your number of classes
    model.load_state_dict(torch.load(model_load_path, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()
    return model


dataset = load_dataset()
normalizer = Normalize(mean=[.485, .456, .406], std=[.229, .224, .225]) # avg of all images RGB

model = load_model()
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Changes images to all be one size
val_transforms = Compose([
    Resize((224, 224)),
    ToTensor(),
    normalizer
])
def prediction(image_path):
    image = Image.open(image_path).convert('RGB')
    image = val_transforms(image).unsqueeze(0)
    image = image.to(DEVICE)
    model.eval()
    with torch.no_grad():
        output = model(image)
        probabilities = nn.functional.softmax(output, dim=1)
        predicted_class = probabilities.argmax().item()
    label = dataset.classes[predicted_class]
    return label
