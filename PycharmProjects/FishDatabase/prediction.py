import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Normalize, RandomHorizontalFlip, Resize, ToTensor
from PIL import Image


Path_to_data = "./fish_dataset"
dataset = ImageFolder(Path_to_data)
normalizer = Normalize(mean=[.485, .456, .406], std=[.229, .224, .225]) # avg of all images RGB

# pre-trained model for image recognition
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
model = resnet18(weights=ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(in_features=512, out_features=36)
model = model.to(DEVICE)

model_load_path = "./fish_model.pth"
model = resnet18(weights=ResNet18_Weights.DEFAULT)  # Initialize model
model.fc = nn.Linear(in_features=512, out_features=36)  # Adjust for your number of classes
model.load_state_dict(torch.load(model_load_path, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

# Changes images to all be one size
val_transforms = Compose([
    Resize((224, 224)),
    ToTensor(),
    normalizer
])
def prediction(image_path, model, transform, device):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)
    image = image.to(device)
    model.eval()
    with torch.no_grad():
        output = model(image)
        probabilities = nn.functional.softmax(output, dim=1)
        predicted_class = probabilities.argmax().item()
    label = dataset.classes[predicted_class]
    return label

image_path = './test.jpg'
predicted_label = prediction(image_path, model, val_transforms, DEVICE)
print(predicted_label)