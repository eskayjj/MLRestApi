from cnnmodel import CNN
import torch
import io
from PIL import Image
from torchvision import transforms

PATH = 'C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/model.pth'

imsize = 28
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

model = CNN(1)
model.load_state_dict(torch.load(PATH))
model.eval()

def prediction(file):
    if file:
        img = Image.open(io.BytesIO(file))
        loadedimg = loader(img)
        loadedimg = loadedimg[0,:,:]
        loadedimg = loadedimg[None,:,:]
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