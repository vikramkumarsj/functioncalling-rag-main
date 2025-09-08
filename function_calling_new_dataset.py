# Use the API to pull new USGS dataset as JSON file as per query filters

from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
#import ollama

import requests
import json

time ='2025-09-01'

api_url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?limit=2&api_key=addyourkey&datetime=2025-09-01"  # Replace with the actual API URL
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
# Process or save the 'data' as needed     
    with open(".//ApiData/USGSData_2025-09-01.json", "w+") as f:
        json.dump(data, f)

        
    print(f"Data for this monitoring location on this {time}")        

else:
    print(f"Error: API request failed with status code {response.status_code}")

