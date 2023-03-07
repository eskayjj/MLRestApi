import uvicorn
import os
import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.predictor import predictor
from app.trainer import trainer
from app.model_to_db import modelToDB
from app.db_to_model import dbToModel
import torch

app = FastAPI()

#Classes to format various key-value pairs and their data-types
class predict(BaseModel):
    filename: str

#API that shows if API is successfully connected 
@app.get('/')   #a get decorator with a base url of "/"
async def homepage():
    message = {"success": True, "message": "Successfully linked to MLAPI"}
    return message

#API to upload a zipfile to the server
@app.post("/uploadmodel/")  #a post decorator with a url of "/uploadmodel/"
def upload_files(file: UploadFile):  
    #Upload files to server and generates a unique ID for each
    try:  
        if os.path.exists("./temp") == True:
            shutil.rmtree("./temp") 
        os.mkdir('./temp')
        os.chdir('./temp')
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        objectID = modelToDB(buffer.name)
        os.chdir('../')
        shutil.rmtree("./temp")
        with open('ids.txt', "a") as f:
            f.write("Filename: " + file.filename + "    Object ID: " + objectID + "\n")
    except Exception as e:
        return{"success": False, "message": str(e)}
    return {"success": True,"filename": file.filename, "objectID": objectID} 

#API that predicts the picture based on existing NN model
@app.post("/predict/")
async def predict(file:predict): 
    result = predictor(file.filename)
    if (result == 'Ant' or result == 'Bee'):
        success = True
    return {"result": result, "success": success}
  
#API that train existing NN model based on new dataset
@app.post("/train/{id}")
async def train(zipFile:UploadFile, id:str):
#Check uploaded content type
    if zipFile.content_type != "application/x-zip-compressed":
        raise HTTPException(400, detail="Invalid document type")
    if type(id) != str:
        raise HTTPException(400, detail="No Valid ID")
    try:
        modelName = dbToModel(id)
        if os.path.exists("./temp") == True:
            shutil.rmtree("./temp") 
        os.mkdir('./temp')
        os.chdir('./temp')
        with open(zipFile.filename, "wb") as buffer:
            shutil.copyfileobj(zipFile.file, buffer)
        trained = trainer(zipFile.filename, modelName)   
        print("Before", os.getcwd())
        if os.path.exists("./temp") == True:
             shutil.rmtree("./temp") 
        os.mkdir('./temp')
        print(os.getcwd())
        shutil.copyfile(os.path.join('./app/' , modelName), os.path.join('./temp/', modelName))
        objectID = modelToDB(modelName)
        shutil.rmtree("./temp")
        with open('ids.txt', "a") as f:
            f.write("Filename: " + modelName + "    Object ID: " + objectID + "\n")
    except Exception as e:
        return{"success": False, "message": str(e)}

    return {"trained": trained}
    
#only runs this file when ran as main file    
if __name__ == "__main__":      
    uvicorn.run(app, host="0.0.0.0", port=8080)