import uvicorn
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, Response
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from predictor import prediction
from trainer import train
import traceback
import pickle
import os
import shutil
import base64
from pathlib import Path
import uuid

app = FastAPI()
app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/uploadfiles/",
        #max_size=1200000,
        file_type=["image/png", "image/jpeg", "image/jfif"]
)

#templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

class Predictor(BaseModel):
    filename: str

class Trainer(BaseModel):
    filename: List[str]


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


# files: List[UploadFile] = File(...)
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    for file in files:
        file.unique_id = str(uuid.uuid4())
    return {"filenames": [file.filename for file in files], "id": [file.unique_id for file in files]} 

@app.post("/predict/{result}")
async def predict(file:Predictor): 
    result = prediction(file.filename)
    return {"result": result}



#change this to display JSON data to HTML
    # try:
    #     contents = file.file.read()
    #     print("1", file.filename)
    #     final = Results(filename=file.filename, result = prediction(contents))
    #     base64_encoded_image = base64.b64encode(contents).decode("utf-8")
    # except Exception:
    #     return {"message": "There was an error uploading the file"}
    # finally:
    #     file.file.close()
    # return {'final': final.dict(), "myImage": base64_encoded_image}
  

@app.post("/train/{trained}")
async def train(file:Trainer):
    fileList = []
    
    if os.path.isdir("./train"):
        os.chdir("..\\")
    print(os.getcwd())

    dir = './trainer/train'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    os.chdir(dir)

    for file_ in file:
        try:
            with open(file_.filename, 'wb') as f:
                while contents := file_.file.read():
                    f.write(contents)  #create a folder to write train data into!
                fileList.append(file_.filename)
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
    # with open('trainset.dat', 'wb') as fl:
    #     pickle.dump(fileList, fl) 

    print(os.getcwd())
    trained = train(dir, fl)

    return {"trained": trained}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)