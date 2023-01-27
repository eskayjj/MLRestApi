from cnnmodel import CNN
from typing import Any
import torch
import io
import numpy as np
from PIL import Image
from torchvision import transforms

PATH = 'C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/model.pth'

#final = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}

#img = Image.open('C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/tester.png').convert('RGB')
#print(img.size)
imsize = 28
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])
#loadedimg = loader(img)
#print(loadedimg.shape)

model = CNN(1)
model.load_state_dict(torch.load(PATH))
model.eval()

def prediction(file):
    if file:
        img = Image.open(io.BytesIO(file))
        loadedimg = loader(img)
        loadedimg = loadedimg[0,:,:]
        #print(loadedimg.shape)
        loadedimg = loadedimg[None,:,:]
        #print(loadedimg.shape)
        predicts = model(loadedimg) 
        predicts = predicts.argmax(axis=1)
        predicts = predicts.item()
        for i in range(9):
            if predicts == i:
                print("This is prediction:", predicts)
            else:
                continue 
    else: 
        raise Exception("Need an image input!")   
    return predicts  