import requests
import traceback

url = "http://localhost:8000"

new_picture = {
    "filename": 'C:/Users/User/AStar Intern/Prototype/RESTApi/Dataset/AntBee/train/ants/Ant_1.jpg'  #serialise this address
}

try:
    response = requests.post(f"{url}/predict", json=new_picture)
except:
    traceback.print_exc()
    print(Exception)
finally:
    print(response.json())

