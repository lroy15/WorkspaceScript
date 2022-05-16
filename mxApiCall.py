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
    'Authorization': 'Bearer '+os.environ.get("API_KEY")
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    #Pull info from Procedures

    parsed = json.loads(response.text)

    num_of_fields = 4
    
    field_data = []

    for x in range(num_of_fields):
    
        field_data.append(parsed["workOrder"]["procedure"]["fields"][x]["value"]["text"])
        
    

    class MxUser:
        def __init__(self, name, title, department, email):
            self.name = name
            self.title = title
            self.department = department
            self.email = email

    return MxUser(field_data[0], field_data[1], field_data[2], field_data[3])

    

    

