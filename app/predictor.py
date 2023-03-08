import torch
import torchvision
import os
import io
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import ResNet18_Weights

#Existing local directory of model, needs to be dynamic for deployment
#PATH = './app/model.pth'

imsize = 256    #This value has to be dynamic based on the tensor length of the model
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

def predictor(fileName, modelName):
    #Loads the model and ensures that CUDA is available and used
    model = torchvision.models.resnet18(weights = ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)
    print(torch.cuda.is_available())
    #print(os.getcwd())
    model.load_state_dict(torch.load(os.path.join('../app/', modelName)))
    model.eval()

    print(fileName)                         
    if fileName:  
        img = Image.open(fileName)
        loadedimg = loader(img)
        loadedimg = loadedimg.unsqueeze(0)
        predicts = model(loadedimg) 

        #Each output node is given an integer to classify            
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