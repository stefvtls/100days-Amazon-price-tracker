import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()
email = os.getenv("EMAIL")
email2 = os.getenv("EMAIL2")
pas = os.getenv("PAS")
price_limit = 200

URL = "https://www.amazon.com/Delonghi-EC680R-DEDICA-Espresso-Machine/dp/B01CEBJUBW/ref=sr_1_20?crid=2CUBT9008EWBF&keywords=espresso%2Bdelonghi%2Bmachine&qid=1655722916&sprefix=espresso%2Bde%2Blongi%2Bmachine%2Caps%2C154&sr=8-20&th=1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
response = requests.get(url=URL, headers=HEADERS)
response.raise_for_status()
print(response.status_code)
bullion = response.text
# print(bullion)

soup = BeautifulSoup(bullion, "html.parser" )
price = soup.find(name="span", class_="a-offscreen")
price_string = price.text.split("$")[1]
price_float = float(price_string)
print(price_float)
title = soup.find(name="span", id="productTitle")
title_text = title.text.strip()
print(title_text)

if price_float <= price_limit:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(password=pas, user=email)
        connection.sendmail(from_addr=email, to_addrs=email2, msg=f"Subject: Price alert!\n\n"
                                                                  f"{title_text} for only {price_float}\n buy now here: \n {URL}")
        print("Email has been sent")
else:
    print("Price too high. Email has not been sent")