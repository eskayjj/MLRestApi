import uvicorn
import aiofiles
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, Response
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from predictor import prediction
from trainer import train

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Number(BaseModel):
    number:int


@app.get('/') #double decorator
@app.get('/home', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.post("/predict")
async def predict(request: Request, files: UploadFile = File(...)):
    contents = await files.read()
    result = prediction(contents)
    return templates.TemplateResponse('predict.html', {'request': request, 'result': result})

@app.post("/train")
async def predict(response: Response):
    test_final = response
    if test_final:
        print("TRAINING DONE")
    else:
        print("ERROR")
    return templates.TemplateResponse('traindataset.html', {'response': response, 'test_final': test_final})

@app.post("/upload")
async def upload(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = await file.read()
            async with aiofiles.open(file.filename, 'wb') as f:
                await f.write(contents)
        except Exception:
            return("Error in file upload")
        finally:
            await file.close()
    return{"message": f"Successfully uploaded {[file.filename for file in files]}", 'request': request}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)