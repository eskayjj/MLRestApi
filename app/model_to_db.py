import io
from gridfs import GridFS
from pymongo import MongoClient
from decouple import config

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017

#Retrieving environment variables
username = config('user', default='')
password = config('password', default='')
clusterAdd = config('clusterAdd', default='')
MONGO_DB = "Cluster0"

# Using GridFS to chunk a large model file into MongoDB
def modelToDB(fileName):
    #Connecting to MongoDB Atlas and creating a GridFS object
    con = MongoClient(f"mongodb+srv://{username}:{password}@{clusterAdd}/?retryWrites=true&w=majority")
    db = con[MONGO_DB]
    fs = GridFS(db)

    #Prevents duplicate models from passing into DB
    print("FileName: ", fileName)
    query = fs.find_one({"filename" : fileName}) # equivalent to find_one
    
    if query:
        iD = query._id
        print(iD)

        if(fs.exists(_id = iD)):
            fs.delete(iD)
    with io.FileIO(fileName,'r') as fileObject:
        objectId = fs.put(fileObject, filename = fileName)
    return str(objectId)