import os
import requests
from dotenv import load_dotenv
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.base_url=os.environ["SHEETY_BASE"]
        self.prices_url=os.environ["PRICES_ENDPOINT"]
        self.users_url=os.environ["USERS_ENDPOINT"]
        self.headers={
            "Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}",
            "Content-Type": "application/json",
        }

    def retrieve_sheety_data(self):
        sheet_response = requests.get(url=self.prices_url, headers=self.headers)
        sheet_response.raise_for_status()
        return sheet_response.json()

    def get_customer_emails(self):
        users_response=requests.get(url=self.users_url,headers=self.headers)
        users_response.raise_for_status()
        return users_response.json()

    def insert_IATA_Code(self, id, code):
        sheety_put_endpoint = f"{self.base_url}/{id}"
        body = {
            "price": {
                "iataCode": code
            }
        }
        response = requests.put(sheety_put_endpoint, json=body, headers=self.headers)
        response.raise_for_status()