import uvicorn
import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.predictor import predictor
from app.trainer import trainer

app = FastAPI()

#Classes to format various key-value pairs and their data-types
class predict(BaseModel):
    filename: str

class train(BaseModel):
    zipname: str

#API that shows if API is successfully connected 
@app.get('/')   #a get decorator with a base url of "/"
async def homepage():
    message = {"success": True, "message": "Successfully linked"}
    return message

#API to upload a zipfile to the server
@app.post("/uploadfiles/")  #a post decorator with a url of "/uploadfiles/"
async def upload_files(zipFile: UploadFile):
    
    #Check uploaded content type
    if zipFile.content_type != "application/x-zip-compressed":
        raise HTTPException(400, detail="Invalid document type")
    
    #Mimics database
    print(os.getcwd()) 
    os.chdir("./app/trainer")   
    print(os.getcwd())

    #Upload files to server and generates a unique ID for each
    file = zipFile
    try:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file.unique_id = str(uuid.uuid4())  
    except Exception as e:
        return{"message": e}
    return {"success": True,"filename": file.filename, "id": file.unique_id} 

#API that predicts the picture based on existing NN model
@app.post("/predict/")
async def predict(file:predict): 
    result = predictor(file.filename)
    return {"result": result}
  
#API that train existing NN model based on new dataset
@app.post("/train/")
async def train(file:train):
    trained = trainer(file.zipname)
    return {"trained": trained}
    
#only runs this file when ran as main file    
if __name__ == "__main__":      
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)