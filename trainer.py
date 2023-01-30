import torch
import io
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights



PATH = 'C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/abmodel.pth'

imsize = 256
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

model = resnet18(ResNet18_Weights.DEFAULT)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(PATH))
model.eval()

def train(file):
    if file:
        img = Image.open(io.BytesIO(file))
        torch.save(model.state_dict(), PATH)
    else:
        raise Exception("File Error")
   
   