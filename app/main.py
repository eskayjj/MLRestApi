import uvicorn
import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from app.predictor import predictor
from app.trainer import trainer
#from starlette.templating import Jinja2Templates

#Basic declaration for an calling a FastAPI object
app = FastAPI()
# app.add_middleware(
#         ValidateUploadFileMiddleware,
#         app_path="/uploadfiles/",
#         #max_size=1200000,
#         file_type=["application/zip", "image/jpeg", "image/png", "image/jfif"]
# )

#templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

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

#API to upload files to the server
@app.post("/uploadfiles/")  #a post decorator with a url of "/uploadfiles/"
async def upload_files(files: List[UploadFile] = File(...)):
    
    #Mimics server file
    print(os.getcwd()) 
    os.chdir("./trainer")   
    print(os.getcwd())

    #Upload files to server and generates a unique ID for each
    for file in files:
        try:
            with open(file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file.unique_id = str(uuid.uuid4())  
        except Exception as e:
            return{"message": e}
    return {"filenames": [file.filename for file in files], "id": [file.unique_id for file in files]} 

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