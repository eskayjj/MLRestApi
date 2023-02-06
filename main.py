import uvicorn
import aiofiles
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, Response
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from predictor import prediction
from trainer import train
import traceback
import pickle
import os
import shutil
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

@app.get('/') #double decorator
@app.get('/home', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.post("/predict")
async def predict(request: Request, files: UploadFile = File(...)):
    contents = await files.read()
    result = prediction(contents)
    return templates.TemplateResponse('predict.html', {'request': request, 'result': result})
  

@app.post("/upload")
async def upload(response: Response, request: Request, files: List[UploadFile] = File(...)):
    fileList = []
    predicted = True
    
    if os.path.isdir("./train"):
        os.chdir("..\\")
    print(os.getcwd())
    
    dir = './trainer/train'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    os.chdir(dir)

    for file in files:
        try:
            with open(file.filename, 'wb') as f:
                while contents := file.file.read():
                    f.write(contents)  #create a folder to write train data into!
                fileList.append(file.filename)
                print(fileList)

            w = open('filelist.txt', 'w')
            w.write(str(fileList))
            w.close()

        except Exception:
            traceback.print_exc()
            return("Error in file upload")
        finally:
            file.file.close()  
    print(fileList)
    with open('trainset.dat', 'wb') as fl:
        pickle.dump(fileList, fl) 

    print(os.getcwd())
    train(dir, fl)

    if(predicted):
            return templates.TemplateResponse('traindataset.html', {'test_final': predicted, 'request': request})
    return{"message": f"Successfully uploaded {[file.filename for file in files]}", 'response': response}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)