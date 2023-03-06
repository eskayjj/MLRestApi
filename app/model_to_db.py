import io
from gridfs import GridFS
from pymongo import MongoClient

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017
MONGO_DB = "Cluster0"


# Using GridFS to chunk a large model file into MongoDB
def modelToDB(fileName):
    con = MongoClient("mongodb+srv://eskayjj:mcdiyMzQ8FagUkax@cluster0.v6l9bv7.mongodb.net/?retryWrites=true&w=majority")
    db = con[MONGO_DB]
    fs = GridFS(db)

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