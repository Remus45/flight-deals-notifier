import requests
import os
from datetime import datetime, timedelta

class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, t):
        self.base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self.token = t
        self.origin_code = os.getenv("ORIGIN_IATA", "TRV")
        self.stops = 0  # added: how many stops the chosen flight has

    def check_flights(self, origin_city_code, destination_city_code, departure_date, is_direct=True):
        """
        Returns a list of offers (JSON) for a given date and direct/indirect constraint.
        """
        headers_amadeus_api = {
            "Authorization": f"Bearer {self.token}",
        }
        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": departure_date,
            "adults": 1,
            # IMPORTANT: nonStop must be a **string** "true"/"false" for Amadeus
            "nonStop": "true" if is_direct else "false",
        }
        resp = requests.get(self.base_url, headers=headers_amadeus_api, params=params)
        resp.raise_for_status()
        return resp.json().get("data", [])

    def search_flight_deal(self, row_data, notification_obj, email_list):
        for row in row_data:
            date_and_cost_dict = {}

            # collect prices for a window of 6 months(180 days)
            for n in range(2):
                dep_date = (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")

                # 1) Try DIRECT first
                origin = row.get("originCode", self.origin_code)  # per-row origin if present; else .env

                offers = self.check_flights(origin, row["iataCode"], dep_date, is_direct=True)

                # 2) If none, try INDIRECT
                if not offers:
                    offers = self.check_flights(origin, row["iataCode"], dep_date, is_direct=False)

                # If still none, skip this date
                if not offers:
                    continue

                # Find the cheapest offer for this date
                cheapest = min(offers, key=lambda o: float(o["price"]["grandTotal"]))
                fare = float(cheapest["price"]["grandTotal"])
                currency = cheapest["price"].get("currency", "EUR")

                # derive stops and final destination from itineraries/segments
                segments = cheapest["itineraries"][0]["segments"]
                self.stops = max(0, len(segments) - 1)
                # final arrival airport code (last segment arrival)
                final_dest_code = segments[-1]["arrival"]["iataCode"]

                # confirm the date from the first segment departure
                dep_iso = segments[0]["departure"]["at"]
                dep_date_confirm = dep_iso.split("T")[0]

                # store cheapest for that date
                date_and_cost_dict[dep_date_confirm] = {
                    "price": fare,
                    "currency":currency,
                    "stops": self.stops,
                    "final_dest": final_dest_code,
                }
                print(f"Day{n} completed")

            print(date_and_cost_dict)

            # Guard if no dates had offers
            if not date_and_cost_dict:
                print(f"No offers found for {row['city']} ({row['iataCode']}), skipping.")
                continue

            # Get the absolute cheapest date overall
            best_date = min(date_and_cost_dict, key=lambda d: date_and_cost_dict[d]["price"])
            best = date_and_cost_dict[best_date]
            lowest_fare = best["price"]

            if lowest_fare < row["lowestPrice"]:
                notification_obj.send_cheap_deal_sms(
                    origin,
                    best["final_dest"],  # final destination airport, not stopover
                    best["currency"],
                    lowest_fare,
                    best_date,
                    best["stops"]
                )
                notification_obj.send_emails(
                    email_list,
                    origin,
                    best["final_dest"],
                    best["currency"],
                    lowest_fare,
                    best_date,
                    best["stops"]
                )