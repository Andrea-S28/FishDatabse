from PycharmProjects.FishDatabase.prediction import load_dataset, prediction, load_model, get_model_path
import torch.nn as nn
import os

def test_prediction():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(script_dir, 'sample_fish.jpg')

    if not os.path.exists(image):
        raise FileNotFoundError(f'Sample image not found: {image}')

    image_test = prediction(image)
    assert image_test == '21', f"Expected 21 got '{image_test}'"
    print('test_prediction passed')

def test_load_dataset():
    dataset = load_dataset()
    assert len(dataset) > 0, 'Dataset should not be empty.'
    print(f'Dataset loaded succesfully with {len(dataset)} images')

def test_get_model_path():
    model_path = get_model_path()
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../FishDatabase')
    model_rel_path = os.path.relpath(model_path, base_dir)
    expected_rel_path = 'fish_model.pth'
    assert model_rel_path == expected_rel_path, f"Expected {expected_rel_path}, but got {model_rel_path}"
    print(f'test_get_model_path passed')

def test_load_model():
    model = load_model()
    assert isinstance(model, nn.Module), f'Expected: nn.Module, Received: {type(model)}'
    expected_classes = 36
    assert model.fc.out_features == expected_classes, f'Expected 36, Received: {model.fc.out_features}'
    print('test_load_model passed')

test_load_dataset()
test_prediction()
test_get_model_path()
test_load_model()