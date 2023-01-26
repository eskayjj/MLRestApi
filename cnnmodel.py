import torch
from numpy import vstack
from numpy import argmax
from sklearn.metrics import accuracy_score
from torchvision.datasets import MNIST
from torchvision.transforms import Compose
from torchvision.transforms import ToTensor
from torchvision.transforms import Normalize
from torch.utils.data import DataLoader
from torch.nn import Conv2d
from torch.nn import MaxPool2d
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Softmax
from torch.nn import Module
from torch.optim import SGD
from torch.nn import CrossEntropyLoss
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_
import torch.nn.functional as F

#Check for GPU CUDA
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#print(device)

#Prepare Dataset
path = 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset'
trans = Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])
train = MNIST(path, train = True, download = True, transform = trans)
test = MNIST(path, train = False, download = True, transform = trans)
kwargs = {'num_workers': 1, 'pin_memory': True}
train_dl = DataLoader(train, batch_size = 64, shuffle = True, **kwargs)
test_dl = DataLoader(test, batch_size = 1000, shuffle = True, **kwargs)
print(len(train_dl.dataset), len(test_dl.dataset))

# model definition
class CNN(Module):
    # define model elements
    def __init__(self, N):
        super(CNN, self).__init__()
        # input to first hidden layer
        self.conv1 = Conv2d(N, 32, (3,3))
        kaiming_uniform_(self.conv1.weight, nonlinearity='relu')
        # first pooling layer
        self.pool = MaxPool2d((2,2), stride=(2,2))
        # second hidden layer
        self.conv2 = Conv2d(32, 32, (3,3))
        kaiming_uniform_(self.conv2.weight, nonlinearity='relu')
        # fully connected layer
        self.fc1 = Linear(5*5*32, 100)
        kaiming_uniform_(self.fc1.weight, nonlinearity='relu')
        # output layer
        self.fc2 = Linear(100, 10)
        xavier_uniform_(self.fc2.weight)
        self.act1 = Softmax(dim=1)
 
    # forward propagate input
    def forward(self, X):
        # input to first hidden layer
        X.to(device)
        X = self.pool(F.relu(self.conv1(X)))
        # second hidden layer
        X = self.pool(F.relu(self.conv2(X)))
        # flatten
        X = X.view(-1, 4*4*50)
        # third hidden layer
        X = F.relu(self.fc1(X))
        # output layer
        X = F.relu(self.fc2(X))
        X = self.act1(X)
        return X

if __name__ == "__main__": #this segment of code is not run if not main

    # define the network
    model = CNN(1).to(device)

    # define the optimization
    criterion = CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)    

    # enumerate epochs
    for epoch in range(10):
        # enumerate mini batches
        for i, (inputs, targets) in enumerate(train_dl):
            inputs = inputs.to(device)
            targets = targets.to(device)
            # clear the gradients
            optimizer.zero_grad()
            # compute the model output
            yhat = model(inputs)
            # calculate loss
            loss = criterion(yhat, targets)
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()
            print(device, i, epoch)

    # # evaluate the model
    # def evaluate_model(test_dl, model):
    #     predictions, actuals = list(), list()
    #     for i, (inputs, targets) in enumerate(test_dl):
    #         # evaluate the model on the test set
    #         yhat = model(inputs)
    #         # retrieve numpy array
    #         yhat = yhat.detach().numpy()
    #         actual = targets.numpy()
    #         # convert to class labels
    #         yhat = argmax(yhat, axis=1)
    #         # reshape for stacking
    #         actual = actual.reshape((len(actual), 1))
    #         yhat = yhat.reshape((len(yhat), 1))
    #         # store
    #         predictions.append(yhat)
    #         actuals.append(actual)
    #     predictions, actuals = vstack(predictions), vstack(actuals)
    #     # calculate accuracy
    #     acc = accuracy_score(actuals, predictions)
    #     return acc

    # evaluate the model
    #acc = evaluate_model(test_dl, model)
    #print('Accuracy: %.3f' % acc)

    torch.save(model.state_dict(), 'C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/model.pth')

