from data_manager import DataManager
from flight_search import FlightSearch

def populate_iata_codes():
    dm = DataManager()
    fs = FlightSearch()
    sheet_data = dm.retrieve_sheety_data()
    for row in sheet_data["prices"]:
        city = row["city"]
        row_id = row["id"]
        iata_code = fs.amadeus_city_search(city)
        dm.insert_IATA_Code(row_id, iata_code)
        print(f"Row Updated: {city} → {iata_code}")

if __name__ == "__main__":
    populate_iata_codes()