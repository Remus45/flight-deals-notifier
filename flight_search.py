import os
import requests
from dotenv import load_dotenv
load_dotenv()

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.client_id=os.environ["CLIENT_ID"]
        self.client_secret=os.environ["CLIENT_SECRET"]
        self.token=self.retrieve_amadeus_token()

    def retrieve_amadeus_token(self):
        amadeus_token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"

        headers_amadeus_token = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        amadeus_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(amadeus_token_endpoint, headers=headers_amadeus_token, data=amadeus_data)
        response.raise_for_status()
        token_data = response.json()
        self.token= token_data["access_token"]
        return self.token

    def amadeus_city_search(self, c):
        headers_amadeus_api = {
            "Authorization": f"Bearer {self.token}",
        }
        amadeus_city_search_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        city_search_parameters = {
            "keyword": c,
        }
        response = requests.get(amadeus_city_search_endpoint, params=city_search_parameters,headers=headers_amadeus_api)
        response.raise_for_status()
        search_result = response.json()
        data=search_result.get("data",[])
        if data:
            return data[0]["iataCode"]
        else:
            return "N/A"