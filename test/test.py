import requests
import traceback
import json

url = "http://35.239.210.99:8080/predict/640704fee9e9c81d970e5096" #need domain

#Comment/Uncomment this for use of /predict/ API
# data = open('C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee/train/ants/Ant_1.jpg', 'rb')

# new_picture = {
#     #"id": '640704fee9e9c81d970e5096',
#     "file": data #serialise this address
# }
# files = {'file': ('foo.txt', open('./foo.txt', 'rb'))}
# response = requests.post('http://127.0.0.1:8000/file', files=files)
# print(response)
# print(response.json())

try:
    with open('C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee/train/ants/Ant_1.jpg', 'rb') as f:
        files = {'file': ('Ant_1.jpg', f, 'image/jpeg')}
        response = requests.post(url=url, files=files)
except:
    traceback.print_exc()
    print(Exception)
finally:
    print(response.text)
    response_json = json.loads(response.text)
    value = response_json['result']
    print(value)

#Comment/Uncomment this for use of /train/ API
#newFile = {"filename": 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee.zip'}

# try:
#     response = requests.post(f"{url}/train", json=newFile)
# except:
#     traceback.print_exc()
#     print(Exception)
# finally:
#     print(response.json())



#Comment/Uncomment this for use of /uploadfiles/ API
#newFile = {"filename": 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee.zip'}
# try:
#     response = requests.post(f"{url}/uploadfiles", json=newFile)
# except:
#     traceback.print_exc()
#     print(Exception)
# finally:
#     print(response.json())