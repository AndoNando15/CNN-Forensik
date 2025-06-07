import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn.functional as F

model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load('model/document_cnn.pth', map_location=torch.device('cpu')))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict_document(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = F.softmax(output, dim=1)[0]
        predicted_idx = torch.argmax(probabilities).item()

    classes = ['fake', 'real']
    label = classes[predicted_idx]
    confidence = f"{probabilities[predicted_idx].item() * 100:.2f}%"

    return {
        "label": label,
        "confidence": confidence
    }
