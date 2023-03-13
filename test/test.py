import requests
import traceback

url = "http://127.0.0.1:8080" #need domain

#Comment/Uncomment this for use of /predict/ API
new_picture = {
    "filename": 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee/train/ants/Ant_1.jpg'  #serialise this address
}
# files = {'file': ('foo.txt', open('./foo.txt', 'rb'))}
# response = requests.post('http://127.0.0.1:8000/file', files=files)
# print(response)
# print(response.json())

try:
    response = requests.post(f"{url}/predict", json=new_picture)
except:
    traceback.print_exc()
    print(Exception)
finally:
    print(response.json())

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