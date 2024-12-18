import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Normalize, RandomHorizontalFlip, Resize, ToTensor
from PIL import Image
import os


def load_dataset():
    """
    load_dataset()
    This function loads the custom dataset “fish_dataset”
    from the specified directory and ensures it exists and prepares it for use in training
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Current Directory
    path_to_data = os.path.join(script_dir, '../FishDatabase/fish_dataset')  # Adjust Path
    if not os.path.exists(path_to_data):
        raise FileNotFoundError(f'Dataset path not found: {path_to_data}')

    return ImageFolder(path_to_data)


def get_model_path():
    """
    get _model_path()
    This function gets the absolute path to the pre-trained model “fish_model.pth”,
    used to load model without hardcoding path multiple times
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Current Directory
    path_to_model = os.path.join(script_dir, "fish_model.pth")  # Adjust Path
    # model_load_path = "./fish_model.pth"
    return path_to_model


def load_model():
    """
    load_model()
    This function loads the pre-trained model and adjust it for our dataset and prepares it for evaluation
    """
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
"""calls load_dataset()"""
normalizer = Normalize(mean=[.485, .456, .406], std=[.229, .224, .225])
"""avg of all images RGB"""


model = load_model()
"""Loads ResNet-18 model pre-trained on ImageNet"""
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
"""Specifies whether computations will be performed by GPU or CPU"""

# Changes images to all be one size
val_transforms = Compose([
    Resize((224, 224)),
    ToTensor(),
    normalizer
])
"""Changes images to all be one size"""


def prediction(image_path):
    """
    prediction()
    The predict function uses the trained model and a user input fish and makes a guess on fish’s species.
    """
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
