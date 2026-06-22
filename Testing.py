from fastapi import FastAPI
import requests

app = FastAPI()

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"  # if required by Keka
}

@app.get("/employees")
def get_employees():

    payload = {
        "pagingOptions": {
            "pageIndex": 1,
            "pageSize": 1000
        },
        "filterOptions": {
            "filters": {},
            "searchKey": ""
        },
        "searchableOptions": [],
        "sortingOptions": {
            "orderBy": "displayName",
            "direction": "asc"
        }
    }

    response = requests.post(
        "https://percipere.keka.com/k/default/api/publicprofile/employeedirectory",
        headers=headers,
        json=payload
    )

    # Always return clean JSON
    return response.json()