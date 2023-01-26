from cnnmodel import CNN
from typing import Any
import torch
from PIL import Image
from torchvision import transforms

PATH = 'C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/model.pth'

#img = Image.open('C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/tester.png')

imsize = 28
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

model = CNN(1)
model.load_state_dict(torch.load(PATH))
model.eval()

def prediction(img):
    if img:
        loadedimg = loader(img)
        predicts = model(loadedimg) 
        print("This is prediction:", predicts) 
    else: 
        raise Exception("Need an image input!")   
    return predicts  