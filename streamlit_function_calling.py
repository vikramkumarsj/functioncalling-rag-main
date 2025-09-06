
from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from RAG_with_RetrievalQA import get_ragdata
from vector_data_manager import store_ragdata
#import ollama

import requests
import json

from datetime import date
# Get the current local date
today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

@tool
def get_waterdata(time: str):
    """Fetches data for a given time"""

    api_url = f"https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?limit=2&api_key=csn8dl7yKqFge7gAW6oiofHhlfA0GSIHj5NvL7uC&datetime={formatted_date}"  # Replace with the actual API URL
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    # Process or save the 'data' as needed in new download folder    
        with open("C:/Users/user/Downloads/functioncalling-rag-main/ApiDataNew/USGSData_2025-09-02.json", "w+") as f:
            json.dump(data, f)
        
        datastore = ".//ApiDataNew/"
        store_ragdata(datastore)

        return data.get(time, "Data for this monitoring location")        

    else:
        return(f"Error: API request failed with status code {response.status_code}")



def get_response(prompt: str, use_function_calling: bool):
    messages = [
        SystemMessage("You are a helpful AI assistant on USGS water data on a given time. Answer concisely."),
        HumanMessage(prompt)
    ]
    if use_function_calling:
        model = ChatOllama(model="llama3.2").bind_tools([get_waterdata])
        res = model.invoke(messages)
        messages.append(res)

        for tool_call in res.tool_calls:
            selected_tool = {"get_waterdata": get_waterdata}[tool_call['name'].lower()]
            tool_message = selected_tool.invoke(tool_call)
            print(tool_message)
            messages.append(tool_message)

        #res = model.invoke(messages)
        res = get_ragdata(prompt)
        messages.append(res)
        return res, messages

    else:
        #model = ChatOllama(model="llama3.2")
        #res = model.invoke(messages)
        res = get_ragdata(prompt)
        messages.append(res)
        return res, messages
    

#
#   STREAMLIT
#
import streamlit as st

st.title("USGS Data Analysis")

# Toggle to turn on function calling
use_function_calling = st.toggle("Turn on function calling")

# Prompt input
prompt = st.text_input("Prompt")

# Submit button
if st.button("Submit", type="primary", use_container_width=True):
    with st.spinner():
        res, messages = get_response(prompt, use_function_calling)

        st.write(res)

        with st.expander("Chat messages"):
            st.write(messages)

