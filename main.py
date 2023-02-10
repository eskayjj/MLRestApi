import uvicorn
import aiofiles
from typing import List
from fastapi import FastAPI, Request, File, UploadFile, Response
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, ORJSONResponse
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from predictor import prediction
from trainer import train
import traceback
import pickle
import os
import shutil
import base64
from pathlib import Path

app = FastAPI()
app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/upload/",
        file_type=["image/png", "image/jpeg", "image/jfif"]
)
app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/predict/",
        #max_size=1200000,
        file_type=["image/png", "image/jpeg", "image/jfif"]
)

templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

class Results(BaseModel):
    result: str
    filename: str
# class InputFile(BaseModel):
#     filename: str


@app.get('/') #double decorator
@app.get('/home', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})


# async def predict(inputFile: InputFile):   #change this to display JSON data to HTML
#     try:
#         with open(inputFile.filename, 'rw') as doc:
#             contents = doc.read()
#             print(contents)
#     except Exception as e:
#         return str(e)
#         # return {"message": "There was an error uploading the file"}
#     return {"hi": True}
    # try:
    #     contents = file.file.read()
    #     print(file.filename)
    #     final = Results(filename=file.filename, result=prediction(contents))
    # except Exception:
    #     return {"message": "There was an error uploading the file"}
    # finally:
    #     file.file.close()

    # base64_encoded_image = base64.b64encode(contents).decode("utf-8")
    # return{}

# @app.post("/predict")
# async def predict(request: Request, file: UploadFile):   #change this to display JSON data to HTML
#     try:
#         contents = file.file.read()
#         print(file.filename)
#         final = Results(filename=file.filename, result=prediction(contents))
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()
#     # final.filename = str(file.filename)
#     # final.result = prediction(contents)
#     base64_encoded_image = base64.b64encode(contents).decode("utf-8")
#     return templates.TemplateResponse('predict.html', {'request': request, 'final': final.dict(),  "myImage": base64_encoded_image})

@app.post("/predict")
async def predict(file: UploadFile):   #change this to display JSON data to HTML
    try:
        contents = file.file.read()
        print(file.filename)
        final = Results(filename=file.filename, result = prediction(contents))
        base64_encoded_image = base64.b64encode(contents).decode("utf-8")
    except Exception as e:
        #return str(e)
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    # return {"Test": True}
    return {'final': final.dict(), "success": result,  "myImage": base64_encoded_image}
    # return ORJSONResponse({'final': final.dict(), "success": result,  "myImage": base64_encoded_image})
  

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