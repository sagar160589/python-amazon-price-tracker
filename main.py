import requests, lxml, smtplib, json, html
from bs4 import BeautifulSoup

AMZ_PRD_URL = "https://www.amazon.com/Hamilton-Beach-35035-Capacity-Professional/dp/B073SM2KL1/ref=sr_1_3?c=ts&keywords=Deep+Fryers&qid=1678717493&s=kitchen&sr=1-3&ts_id=289918"
MY_TGT_PRICE = 100

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9'
}
response = requests.get(AMZ_PRD_URL, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
price_text = soup.find(name='span', class_='a-price-whole')
product_title = soup.find(name='span', id='productTitle')
# Send email if the product price is less than or equal to my target price
with open("config.json") as emailconfig:
    email_data = json.load(emailconfig)
    from_email = email_data['from_email']
    password = email_data['password']
    to_email = email_data['to_email']
if int(price_text.get_text().split(".")[0]) <= MY_TGT_PRICE:
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(from_addr=from_email, to_addrs=to_email,
                            msg=f"Subject: Check for the product - "
                                f"{html.unescape(product_title.get_text())}\n\n Buy this product, It's the right time....")
else:
    print("Not the right time to buy product. Price is still high")
