import torch
import torchvision
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import ResNet18_Weights


PATH = './app/model.pth'

imsize = 256
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

model = torchvision.models.resnet18(weights = ResNet18_Weights.DEFAULT)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(PATH))
model.eval()

def predictor(file):  
    print(file)                         
    if file:                                    
        img = Image.open(file)
        loadedimg = loader(img)
        loadedimg = loadedimg.unsqueeze(0)
        predicts = model(loadedimg)             
        predicts = predicts.argmax(axis=1)
        predicts = predicts.item()
        if predicts == 0:
            predicts = "Ant"
            print("Ant")
        elif predicts == 1:
            predicts = "Bee"
            print("Bee")
    else: 
        raise Exception("Need an image input!")   
    return predicts  