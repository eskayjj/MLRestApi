import io
import pymongo, gridfs
from gridfs import GridFS
from pymongo import MongoClient

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017
MONGO_DB = "Cluster0"


# Using GridFS to chunk a large model file into MongoDB
myclient = pymongo.MongoClient("mongodb+srv://eskayjj:mcdiyMzQ8FagUkax@cluster0.v6l9bv7.mongodb.net/?retryWrites=true&w=majority")
db = myclient.test
mydb = myclient[MONGO_DB]
fs = gridfs.GridFS(mydb)
model_name = 'model.pth'

with io.FileIO(model_name, 'r') as fileObject:
    docId = fs.put(fileObject, filename=model_name)