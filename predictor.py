from cnnmodel import CNN
import torch
import io
import torchvision
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights


PATH = './abmodel.pth' #change this to be relative path

imsize = 256
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

model = torchvision.models.resnet18(ResNet18_Weights.DEFAULT)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
model.load_state_dict(torch.load(PATH))
model.eval()

def prediction(file):                           #return JSON data to main.py {filename: , results: }
    if file:                                    #implement Ants and Bees into this and remove numbers MNIST model
        # img = Image.open(io.BytesIO(file))
        img = Image.open(file)
        loadedimg = loader(img)
        loadedimg = loadedimg.unsqueeze(0)
        # loadedimg = loadedimg[0,:,:]
        # loadedimg = loadedimg[None,:,:]
        predicts = model(loadedimg)             #ValueError: expected 4D input (got 3D input)
        # print(predicts) 
        predicts = predicts.argmax(axis=1)
        predicts = predicts.item()
        # print(predicts)
        if predicts == 0:
            predicts = "Ant"
            print("Ant")
        elif predicts == 1:
            predicts = "Bee"
            print("Bee")
    else: 
        raise Exception("Need an image input!")   
    return predicts  