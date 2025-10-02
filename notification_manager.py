import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
from email.mime.text import MIMEText
load_dotenv()

ACCOUNT_SID=os.environ["ACCOUNT_SID"]
AUTH_TOKEN=os.environ["AUTH_TOKEN"]
MY_EMAIL=os.environ["MY_EMAIL"]
EMAIL_PASSWORD=os.environ["EMAIL_PASSWORD"]
SMTP_ADDR=os.environ["SMTP_ADDR"]
TWILIO_FROM = os.environ.get("TWILIO_FROM", "+18457129813")
ALERT_PHONE = os.environ.get("ALERT_PHONE", "+919446606743")


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid=ACCOUNT_SID
        self.auth_token=AUTH_TOKEN
        self.my_email=MY_EMAIL
        self.password=EMAIL_PASSWORD
        self.smtp_addr=SMTP_ADDR


    def send_cheap_deal_sms(self, dep_iataCode, dest_iataCode, currency, flight_price, flight_date, stops):
        # simple currency symbol map (expand as needed)
        symbols = {"EUR": "€", "USD": "$", "GBP": "£", "INR": "₹"}
        symbol = symbols.get(currency, currency+" ")  # fallback: just print code if unknown

        if stops == 0:
            message_body = (
                f"Low price alert! Only {symbol}{flight_price} to fly direct "
                f"from {dep_iataCode} to {dest_iataCode} on {flight_date}"
            )
        else:
            message_body = (
                f"Low price alert! Only {symbol}{flight_price} to fly from {dep_iataCode} to "
                f"{dest_iataCode} on {flight_date} with {stops} stopover(s)"
            )

        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_FROM,
            to=ALERT_PHONE,
        )
        print(message.status)

    def send_emails(self,email_list, dep_iataCode, dest_iataCode, currency, flight_price, flight_date,stops):
            symbols = {"EUR": "€", "USD": "$", "GBP": "£", "INR": "₹"}
            symbol = symbols.get(currency, currency + " ")

            with smtplib.SMTP(self.smtp_addr) as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.password)
                for email in email_list:
                    if stops == 0:
                        message_body = (
                            f"Low price alert! Only {symbol}{flight_price} to fly direct "
                            f"from {dep_iataCode} to {dest_iataCode} on {flight_date}"
                        )
                    else:
                        message_body = (
                            f"Low price alert! Only {symbol}{flight_price} to fly from {dep_iataCode} to "
                            f"{dest_iataCode} on {flight_date} with {stops} stopover(s)"
                        )

                    msg=MIMEText(message_body,_charset="utf-8")
                    msg["Subject"]="Low price alert!"
                    msg["From"]=self.my_email
                    msg["To"]=email

                    connection.sendmail(from_addr=self.my_email,
                                    to_addrs=email,
                                    msg=msg.as_string()
                    )