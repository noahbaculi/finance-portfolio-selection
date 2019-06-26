import requests
from bs4 import BeautifulSoup
import pandas as pd

# install requests
# install requests-html

# create symbols list with all securities to be considered
symbols_list = ["KO", "SYG", "MUB", "MSEGX", "DBA", "DIS", "V", "JPM", "MSFT", "AAPL"]

df = pd.DataFrame()
pd.set_option("display.max_rows", 16)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 200)

df["Symbol"] = symbols_list

# loop through all securities
for security_index in range(len(symbols_list)):
    # scrape Yahoo finance security profile page
    url = "https://finance.yahoo.com/quote/%s/profile?p=%s" % (symbols_list[security_index], symbols_list[security_index])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())  # to examine imported HTML

    # see if security is a fund, otherwise assume company
    try:
        fund_overview = soup.find_all("div", {"class": "Mb(25px)"})[0].find("h3").text.strip()  # look for fund overview section
        if fund_overview == "Fund Overview":
            security_name = soup.find_all("div", {"class": "Mb(20px)"})[0].find("h3").text.strip()
            info_block = soup.find_all("div", {"class": "Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)"})
            try:  # see if security is a special type of fund
                if info_block[5].find("span", {"class": "Fl(start)"}).text.strip() == "Legal Type":
                    security_type = info_block[5].find("span", {"class": "Fl(end)"}).text.strip()
                else:
                    security_type = "Fund..?"
            except:
                raise SystemExit("An unknown error occured with the type of a fund security.")
            security_category = info_block[0].find("span", {"class": "Fl(end)"}).text.strip()

            print("Success - Fund - %s" % symbols_list[security_index])
            print("Success - Fund Type - %s" % security_type)
            print("Success - Fund Cat - %s" % security_category)
        else:
            print("%s had a Yahoo Finance Profile page that could not be analyzed to find a fund overview section." % symbols_list[security_index])
    except AttributeError:
        security_name = soup.find_all("div", {"class": "qsp-2col-profile Mt(10px) smartphone_Mt(20px) Lh(1.7)"})[0].find("h3").text.strip()
        security_type = "Company"
        security_category = soup.find_all("span", {"class": "Fw(600)"})[0].text.strip()
        print("Success - Company - %s" % symbols_list[security_index])
        print("Success - Company Type - %s" % security_type)
        print("Success - Company Cat - %s" % security_category)

    df.at[security_index, "Security"] = security_name  # assign name to dataframe
    df.at[security_index, "Type"] = security_type  # assign type to dataframe
    df.at[security_index, "Category"] = security_category  # category name to dataframe
    print()

print(df)  # print out dataframe
