import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Form
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from predictor import prediction

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Number(BaseModel):
    number:int


@app.get('/') #double decorator
@app.get('/home', response_class=HTMLResponse)
async def homepage(request: Request, title: str):
    return templates.TemplateResponse('home.html', {"request": request})

@app.post("/predict")
async def predict(request: Request, title: str, files: UploadFile = File(...)):
    contents = await files.read()
    result = prediction(contents)
    return templates.TemplateResponse('predict.html', {'request': request, 'result': result})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)