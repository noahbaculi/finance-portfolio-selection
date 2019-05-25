import requests
from bs4 import BeautifulSoup
import pandas as pd
# install requests
# install requests-html

# create symbols list with all securities to be considered
symbols_list = ["KO", "SYG", "MUB", "DIS", "V", "JPM", "MSFT", "AAPL"]

df = pd.DataFrame()

df["Symbol"] = symbols_list

# loop through all securities
for security_index in range(len(symbols_list)):
    # scrape Yahoo finance security profile page
    url = "https://finance.yahoo.com/quote/%s/profile?p=%s" % (symbols_list[security_index], symbols_list[security_index])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())  # to examine imported HTML

    try:  # see if security is a fund, otherwise assume company
        fund_overview = soup.find_all("div", {"class": "Mb(25px)"})[0].find("h3").text.strip()  # look for fund overview section
        if fund_overview == "Fund Overview":
            security_name = soup.find_all("div", {"class": "Mb(20px)"})[0].find("h3").text.strip()
            print("Success - Fund - %s" % symbols_list[security_index])
    except AttributeError:
        security_name = soup.find_all("div", {"class": "qsp-2col-profile Mt(10px) smartphone_Mt(20px) Lh(1.7)"})[0].find("h3").text.strip()
        print("Success - Company - %s" % symbols_list[security_index])
    df.at[security_index, "Security"] = security_name  # assign name to dataframe
    print()

print(df)  # print out dataframe
