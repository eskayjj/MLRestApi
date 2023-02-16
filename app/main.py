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


app = FastAPI()
# app.add_middleware(
#         ValidateUploadFileMiddleware,
#         app_path="/uploadfiles/",
#         #max_size=1200000,
#         file_type=["application/zip", "image/jpeg", "image/png", "image/jfif"]
# )

#templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

class predict(BaseModel):
    filename: str

class train(BaseModel):
    zipname: str


@app.get('/', response_class=HTMLResponse)
async def homepage():
    content = """
<div>
<h1>Home Page</h1>
</div>
<div>
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit" value="Upload Photo/Photos">
</form>
</body>
</div>
    """
    return HTMLResponse(content=content)


@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    print(os.getcwd()) 
    os.chdir("./trainer")   #mimics server file
    print(os.getcwd())
    for file in files:
        try:
            with open(file.filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file.unique_id = str(uuid.uuid4())  
        except Exception as e:
            return{"message": e}
    return {"filenames": [file.filename for file in files], "id": [file.unique_id for file in files]} 

@app.post("/predict/")
async def predict(file:predict): 
    result = predictor(file.filename)
    return {"result": result}
  

@app.post("/train/")
async def train(file:train):
    trained = trainer(file.zipname)
    return {"trained": trained}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)