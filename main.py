from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from dotenv import load_dotenv
load_dotenv()

def main():
    dm = DataManager()
    fs = FlightSearch()

    sheet_data = dm.retrieve_sheety_data()
    print(sheet_data)

    fd = FlightData(fs.token)
    nm = NotificationManager()
    users_data = dm.get_customer_emails()
    print(users_data)

    email_list = [email["whatIsYourEMailId ?"] for email in users_data["users"]]
    print(email_list)

    fd.search_flight_deal(sheet_data["prices"], nm, email_list)

if __name__ == "__main__":
    main()