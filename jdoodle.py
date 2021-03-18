
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


#linkleri tutmak için
url_list = []

prices_list = []

propKeys = []
propValues = []
 
for i in range(1, 25):
    url = "https://www.trendyol.com/laptop?qt=bilgisayar&st=bilgisayar&pi="+ str(i)
    r = requests.get(url)

    source = BeautifulSoup(r.content, "lxml")
   
    urls = source.find_all("div", attrs={"class": "p-card-chldrn-cntnr"})
    for url in urls:
        url_laptop = "https://www.trendyol.com/"+url.a.get("href")
        url_list.append(url_laptop)
        print(url_laptop)
        
        laptop_link = requests.get(url_laptop)
        source_laptop = BeautifulSoup(laptop_link.content, "lxml")
        
        properties = source_laptop.find_all("div", attrs = {"class":"prop-item"})
        for prop in properties:
            prop_keys = prop.find("div", attrs = {"class":"item-key"}).text
            prop_values = prop.find("div", attrs = {"class":"item-value"}).text
            propKeys.append(prop_keys)
            propValues.append(prop_values)
            
    prices = source.find_all("div", attrs = {"class":"prc-box-sllng"})
    for price in prices:
        prices_list.append(price.text)
        print(price.text)
        
        
        print(str(len(url_list))+ "adet link bulundu")
        print(str(len(prices_list))+ "adet fiyat bulundu")
        print(str(len(propKeys))+ "adet özellik başlığı bulundu")
        print(str(len(propValues))+ "adet özellik değeri bulundu")


df_url = pd.DataFrame()
df_url["urls"] = url_list
df_url["price"] = prices_list

df_url.head()
laptops = len(url_list)
columns = np.array(propKeys)
columns = np.unique(columns)
df = pd.DataFrame(columns=columns)
df["urls"] = url_list
df["prices"] = prices_list
df.head()
for i in range(0, laptops):
    url = df['urls'].loc[i]
    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")
    
    properties = source.find_all("div", attrs={"class":"prop-item"})
    for prop in properties:
        prop_keys = prop.find("div", attrs={"class":"prop-key"}).text
        prop_values = prop.find("div", attrs={"class":"prop-value"}).text
        print(prop_keys+prop_values)
        df[prop_keys].loc[i] = prop_values
df.head()

df.to_csv("C:/Users/tasne/thing/laptop_data.csv", index=False)