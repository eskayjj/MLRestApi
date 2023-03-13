import os
from bson import ObjectId
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

#Using GridFS to retrieve a model from the database
def dbToModel(id):
    #Connecting to MongoDB Atlas and creating a GridFS object
    con = MongoClient(f"mongodb+srv://{username}:{password}@{clusterAdd}/?retryWrites=true&w=majority")
    db = con[MONGO_DB]
    fs = GridFS(db)
    
    try:
        #Source for the model based on input ID and saved on local machine
        modelName = db.fs.files.find_one({'_id': ObjectId(id)})
        print("id", modelName)
        modelName = str(modelName.get('filename')) 
    except Exception as e:
        return(str(e))
    print(os.getcwd())
    os.chdir('./app')
    with open(modelName, 'wb') as fileObject:
        fileObject.write(fs.get(ObjectId(id))
                        .read())
    os.chdir('../')
    return(modelName)