import requests
from requests_testadapter import Resp
import os
import base64

url = "http://localhost:8000"

new_picture = {
    "filename": 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee/train/ants/Ant_1.jpg'  #serialise this address
}


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)

requests_session = requests.session()
requests_session.mount('file://', LocalFileAdapter())

with open(new_picture["filename"], "rb") as image_file:
    file = base64.b64encode(image_file.read())
    
picture = {"file": (new_picture["filename"], file)}

requests_session.post(f"{url}/predict", files=picture)
#response = requests.post(f"{url}/predict", files=picture)

print(requests_session.json())