import uvicorn
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from fastapi import FastAPI, Request, File, UploadFile, Form
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
from predictor import prediction
from PIL import Image

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Number(BaseModel):
    number:int


@app.get('/')
@app.get('/home', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.post("/predict")
def predict(request: Request):
    result = prediction(Image.open('C:/Users/User/AStar Intern/Prototype/RESTApi/FastAPI/tester.png'))
    return templates.TemplateResponse('predict.html', context={'request': request, 'result': result})

@app.post("/uploadfiles/")
async def create_upload_files(
    files: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)