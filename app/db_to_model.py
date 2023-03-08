import os
import pymongo, gridfs
from bson import ObjectId
from gridfs import GridFS
from pymongo import MongoClient

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017
MONGO_DB = "Cluster0"

def dbToModel(id):
    con = MongoClient("mongodb+srv://eskayjj:mcdiyMzQ8FagUkax@cluster0.v6l9bv7.mongodb.net/?retryWrites=true&w=majority")
    db = con[MONGO_DB]
    fs = GridFS(db)
    
    try:
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