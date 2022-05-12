import requests
import json
from dotenv import load_dotenv
import os

def mxGetUser():
    #workorder_ID = input("Enter Workorder ID: ")
    workorder_ID = str(5110369)
    #API call
    url = "https://api.getmaintainx.com/v1/workorders/"+workorder_ID+"?expand=expenditures&expand=expenditures"

    load_dotenv()
    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer '+os.getenv("API_KEY")
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    #Pull info from Procedures

    api_dict = response.text

    parsed = json.loads(api_dict)

    num_of_fields = 4
    

    field_array = []

    for x in range(num_of_fields):
    
        field_array.append(parsed["workOrder"]["procedure"]["fields"][x]["value"]["text"])
        
    

    class MxUser:
        def __init__(self, name, title, department, email):
            self.name = name
            self.title = title
            self.department = department
            self.email = email

    p1 = MxUser(field_array[0], field_array[1], field_array[2], field_array[3])


    
    return p1