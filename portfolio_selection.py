from bs4 import BeautifulSoup
from yahoo_fin.stock_info import *

# install requests
# install requests-html

# create symbols list with all securities to be considered
symbols_list = ["KO", "SPY", "MUB", "MSEGX", "DBA", "DIS", "V", "JPM", "MSFT", "AAPL"]

df = pd.DataFrame(columns=["Symbol", "Security", "Type", "Category", "Price"])
pd.set_option("display.max_rows", 16)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 200)

df["Symbol"] = symbols_list

# loop through all securities
for security_index in range(len(symbols_list)):
    # scrape Yahoo finance security profile page
    url_profile = "https://finance.yahoo.com/quote/%s/profile?p=%s" % (symbols_list[security_index], symbols_list[security_index])
    page_profile = requests.get(url_profile)
    soup_profile = BeautifulSoup(page_profile.content, "html.parser")
    # print(soup_profile.prettify())  # to examine imported profile HTML

    # see if security is a fund, otherwise assume company
    try:  # FUND
        fund_overview = soup_profile.find_all("div", {"class": "Mb(25px)"})[0].find("h3").text.strip()  # look for fund overview section
        if fund_overview == "Fund Overview":
            security_name = soup_profile.find_all("div", {"class": "Mb(20px)"})[0].find("h3").text.strip()
            info_block = soup_profile.find_all("div", {"class": "Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)"})
            try:  # see if security is a special type of fund
                if info_block[5].find("span", {"class": "Fl(start)"}).text.strip() == "Legal Type":
                    security_type = info_block[5].find("span", {"class": "Fl(end)"}).text.strip()
                else:
                    security_type = "Fund..?"
            except:
                raise SystemExit("An unknown error occured with the type of a fund security.")
            security_category = info_block[0].find("span", {"class": "Fl(end)"}).text.strip()
            df.at[security_index, "52-Week Change"] = "-"

            print("Success - Fund - %s" % symbols_list[security_index])
            print("Success - Fund Type - %s" % security_type)
            print("Success - Fund Cat - %s" % security_category)
        else:
            print("%s had a Yahoo Finance Profile page that could not be analyzed to find a fund overview section." % symbols_list[security_index])

    except AttributeError:  # COMPANY
        security_name = soup_profile.find_all("div", {"class": "qsp-2col-profile Mt(10px) smartphone_Mt(20px) Lh(1.7)"})[0].find("h3").text.strip()
        security_type = "Company"
        security_category = soup_profile.find_all("span", {"class": "Fw(600)"})[0].text.strip()
        print("Success - Company - %s" % symbols_list[security_index])
        print("Success - Company Type - %s" % security_type)
        print("Success - Company Cat - %s" % security_category)

        # scrape Yahoo finance security statics page
        url_stats = "https://finance.yahoo.com/quote/%s/key-statistics?p=%s" % (symbols_list[security_index], symbols_list[security_index])
        page_stats = requests.get(url_stats)
        soup_stats = BeautifulSoup(page_stats.content, "html.parser")
        # print(soup_stats.prettify())  # to examine imported profile HTML

        # examine 2 locations for 52 week change parameter
        try:
            if soup_stats.find_all("span", {"data-reactid": "287"})[0].text.strip() == "52-Week Change":
                df.at[security_index, "52-Week Change"] = soup_stats.find_all("td", {"class": "Fz(s) Fw(500) Ta(end)"})[
                    32].text.strip()
            else:
                print("The 52-Week Change parameter at %s is not in the expected location." % url_stats)
        except IndexError:
            try:
                if soup_stats.find_all("span", {"data-reactid": "292"})[0].text.strip() == "52-Week Change":
                    df.at[security_index, "52-Week Change"] = soup_stats.find_all("td", {"class": "Fz(s) Fw(500) Ta(end)"})[32].text.strip()
                else:
                    print("The 52-Week Change parameter at %s is not in the expected location." % url_stats)
            except IndexError:
                pass

        # add Trailing P/E parameter
        if soup_stats.find_all("span", {"data-reactid": "29"})[1].text.strip() == "Trailing P/E":
            df.at[security_index, "Trailing P/E"] = soup_stats.find_all("td", {"class": "Fz(s) Fw(500) Ta(end)"})[2].text.strip()

    df.at[security_index, "Security"] = security_name  # assign name to dataframe
    df.at[security_index, "Type"] = security_type  # assign type to dataframe
    df.at[security_index, "Category"] = security_category  # assign category name to dataframe
    df.at[security_index, "Price"] = "%.2f" % (get_live_price(symbols_list[security_index]))  # get and assign price to dataframe
    print()

print(df)  # print out dataframe
