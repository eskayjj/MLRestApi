import io
import pymongo, gridfs
from bson import ObjectId

# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27017
MONGO_DB = "Cluster0"

con = pymongo.MongoClient("mongodb+srv://eskayjj:mcdiyMzQ8FagUkax@cluster0.v6l9bv7.mongodb.net/?retryWrites=true&w=majority")
db = con.test
db = con[MONGO_DB]
fs = gridfs.GridFS(db)

with open('model.pth', 'wb') as fileObject:
    fileObject.write(fs.get(ObjectId(docId))
                     .read() )