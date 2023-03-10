import torch
import torch.nn as nn
import torch.optim as optim
import shutil
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import datasets, transforms
from torch.optim import lr_scheduler
import time
from zipfile import ZipFile
import copy
import os
import io
import pymongo, gridfs
from gridfs import GridFS
from pymongo import MongoClient


groupId = '63f71e18e441883061675b2b'
clusterName = 'Cluster0'

#Existing local directory of model, needs to be dynamic for deployment
#PATH = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/{groupId}/clusters/{clusterName}/fts/indexes'                    

imsize = 256    #This value has to be dynamic based on the tensor length of the model
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def trainer(dataset_zdir, modelName):

    #Extract the data within the zip file into a local directory (need to change to server database for production)
    print("Dataset_zdir", dataset_zdir) 
    print("Before", os.getcwd())
    with ZipFile(dataset_zdir, 'r') as zObject: # Extracting all the members of the zip into a specific location.
        zObject.extractall(path=os.getcwd())  
        print("Zipfile Name:", os.getcwd())
        unzip_Zobject = str(os.getcwd())+"\\"+str(os.path.basename(dataset_zdir)).removesuffix('.zip') 
        print("New filename:", unzip_Zobject) 
        zObject.close()
        os.chdir("../")
    print("Final directory:", os.getcwd())

    #Training existing model using new dataset
    dataset_dir = unzip_Zobject
    print("Dataset Dir:", dataset_dir)
    print("Current Dir:", os.getcwd())
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    }

    image_datasets = {x: datasets.ImageFolder(os.path.join(dataset_dir, x),
                                          data_transforms[x])
                for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                             shuffle=True, num_workers=4)
              for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    #class_names = image_datasets['train'].classes

    def train_models(model, criterion, optimizer, scheduler, num_epochs=10):
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    
                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

            print()

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))

        # load best model weights
        model.load_state_dict(best_model_wts)
        return model

    model_conv = resnet18(weights = ResNet18_Weights.DEFAULT)
    for param in model_conv.parameters():
        param.requires_grad = False
    num_ftrs = model_conv.fc.in_features
    model_conv.fc = nn.Linear(num_ftrs, 2)
    
    model_conv.load_state_dict(torch.load(os.path.join('./app/', modelName)))
    model_conv.eval()
                                        
    num_ftrs = model_conv.fc.in_features
    model_conv.fc = nn.Linear(num_ftrs, 2)  

    model_conv = model_conv.to(device)    

    criterion = nn.CrossEntropyLoss()

    optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.0001, momentum=0.9)

    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=5, gamma=0.1)
    
    model_conv = train_models(model_conv, criterion, optimizer_conv,
                        exp_lr_scheduler, num_epochs=10)
    
    torch.save(model_conv.state_dict(), os.path.join('./app/', modelName))

    return ("Success")