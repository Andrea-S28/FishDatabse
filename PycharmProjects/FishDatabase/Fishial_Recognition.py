"""
followed this video for image recognition:
https://www.youtube.com/watch?v=QyN_1ep1J1E&t=22s
"""
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Normalize, RandomHorizontalFlip, Resize, ToTensor
import numpy as np
from tqdm import tqdm


Path_to_data = "./fish_dataset"
"""Specifies file path to dataset of fish images"""
dataset = ImageFolder(Path_to_data)
"""creates an ImageFolder object that automatically labels images based on folder"""
normalizer = Normalize(mean=[.485, .456, .406], std=[.229, .224, .225])
"""avg of all images RGB"""


train_transforms = Compose([
    Resize((224, 224)),
    RandomHorizontalFlip(),
    ToTensor(),
    normalizer
])
"""Changes images to all be one size"""

val_transforms = Compose([
    Resize((224, 224)),
    ToTensor(),
    normalizer
])
"""Changes images to all be one size"""

train_samples, test_samples = int(.7 * len(dataset)), len(dataset) - int(.7 * len(dataset))
"""splits data into train and validate sizes"""
train_dataset, val_dataset = torch.utils.data.random_split(dataset, lengths=[train_samples, test_samples])
"""takes both samples and randomly sorts them"""
train_dataset.dataset.transform = train_transforms
"""makes sure each image is transformed to preset"""
val_dataset.dataset.transform = val_transforms


# pre-trained model for image recognition
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
"""Specifies whether computations will be performed by GPU or CPU"""
model = resnet18(weights=ResNet18_Weights.DEFAULT)
"""Loads ResNet-18 model pre-trained on ImageNet"""
model.fc = nn.Linear(in_features=512, out_features=36)
model = model.to(DEVICE)

for name, param in model.named_parameters():
    if 'fc' not in name:
        param.requires_grad_(False)


# Training inputs
optimizer = optim.AdamW(params=model.parameters())
"""The AdamW optimizer updates the models weights during training"""
loss_fn = nn.CrossEntropyLoss()
"""Used to measure the difference between models prediction and true label"""
batch_size = 128
"""group size of images processed together"""

# data loaders
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
"""A data loader that shuffles and batches the training dataset"""
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
"""A data loader that shuffles and batches the validation dataset"""


def train(model, device, epochs, optimizer, loss_fn, batch_size, trainloader, valloader):
    """
    Train()
    The train function is used to train and validate the model over a
    specified amount of epochs using both the training and validation data.
    """
    log_training = {'epochs': [],
                    'training loss': [],
                    'training accuracy': [],
                    'validation loss': [],
                    'validation accuracy': []}

    for epoch in range(1, epochs+1):
        print(f'Starting Epoch {epoch}')
        training_losses, training_accuracies = [], []
        validation_losses, validation_accuracy = [], []

        # training data
        for image, label in tqdm(trainloader):
            image, label = image.to(DEVICE), label.to(DEVICE)
            optimizer.zero_grad()
            out = model.forward(image)

            loss = loss_fn(out, label)
            training_losses.append(loss.item())
            predictions = torch.argmax(out, axis=1)
            accuracy = (predictions == label).sum() / len(predictions)
            training_accuracies.append(accuracy)
            loss.backward()
            optimizer.step()

        # validation data
        for image, label in tqdm(valloader):
            image, label = image.to(DEVICE), label.to(DEVICE)
            with torch.no_grad():
                out = model.forward(image)

                loss = loss_fn(out, label)
                validation_losses.append(loss.item())
                predictions = torch.argmax(out, axis=1)
                accuracy = (predictions == label).sum() / len(predictions)
                validation_accuracy.append(accuracy)

        training_loss_mean, training_acc_mean = np.mean(training_losses), np.mean(training_accuracies)
        valid_loss_mean, valid_acc_mean = np.mean(validation_losses), np.mean(validation_accuracy)

        log_training['epochs'].append(epoch)
        log_training['training loss'].append(training_loss_mean)
        log_training['training accuracy'].append(training_acc_mean)
        log_training['validation loss'].append(valid_loss_mean)
        log_training['validation accuracy'].append(valid_acc_mean)

        print(f'Training Loss: {training_loss_mean:.2f}')
        print(f'Training Accuracy: {training_acc_mean:.2f}')
        print(f'Validation Loss: {valid_loss_mean:.2f}')
        print(f'Validation Accuracy: {valid_acc_mean:.2f}')
    # Save the model
    model_save_path = "./fish_model.pth"
    torch.save(model.state_dict(), model_save_path)
    print(f"Model saved to {model_save_path}")

    return log_training, model


log, model = train(model=model,
                   device=DEVICE,
                   epochs=5,
                   optimizer=optimizer,
                   loss_fn=loss_fn,
                   batch_size=batch_size,
                   trainloader=train_loader,
                   valloader=val_loader)
