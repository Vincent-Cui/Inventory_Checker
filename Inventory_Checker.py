'''

Inventory Checker for Walmart & Target
Version:0.1
Author: Vincent Cui, Jinwen Xu

'''


import requests
import bs4
from lxml import html
from bs4 import BeautifulSoup
from distutils.filelist import findall
import requests
import re
import pandas as pd

def Walmart(SKU, ZIP):
    url = 'https://brickseek.com/walmart-inventory-checker/'
    payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}
    df_record = pd.DataFrame(columns=['Store','City','Availability','Quantity'])
    r = requests.post(url, data=payload).text    # Make a POST request with data
    

    bs = BeautifulSoup(r, 'html.parser')
    j=0
    a = bs.find_all('div', class_='table__body')
    if a == []:
        print('No results found in the searched area.')
    else:    
        for tag in bs.find_all('div', class_='table__body'): 
            for i in range(20):
                m_Store = tag.findAll('strong', class_='address-location-name')
                m=str(m_Store)
                if  i < m.count('/strong'):
                    m_s= m_Store[i].get_text().replace("\nWalmart","")
                    m_add = tag.findAll('address',class_="address")
                    m_Address = m_add[i].contents[2]      
                    m_Availability = tag.findAll('span',class_="availability-status-indicator__text")
                    m_a = m_Availability[i].get_text()
                    if m_a =='Out of Stock'or m_a == 'Limited Stock':
                        m_q = str(0)
                        j=j-1
                    else:    
                        m_Quantity = tag.findAll('span',class_="table__cell-quantity")
                        m_q = m_Quantity[j].get_text()[9:]
                    j=j+1
                    df_record = df_record.append({'Store':m_s, 'City':m_Address, 'Availability':m_a, 'Quantity':m_q }, ignore_index=True)
                else:
                    print(df_record)
                    if len(df_record) == 0:
                        print("No result found")
                    print('Thank you for using Inventory Checker Version: 0.1\nReleased on: 19/04/2020\nSource code is available at: https://github.com/Vincent-Cui/Inventory_Checker\nDevelopment Team: Wencong(Vincent) Cui, Jinwen Xu')
                    print()
                    break

def WalmartKeywords(keywords,ZIP):
    url = "http://www.walmart.com/search/?query="
    r = requests.post(url+keywords).text
    bs = BeautifulSoup(r, 'html.parser')
    result = re.findall(r'href="/ip/(.*?)"', str(bs))
    result = [item for item in result if not("#customer-reviews" in item)]
    result = list(dict.fromkeys(result))
    df = pd.DataFrame(result)
    df.columns = {"product"}
    df[['product','sku']] = df['product'].str.split("/",expand=True) 
    df['product'] = df['product'].str.replace("-"," ")
    for resultitem in range(0,len(df)):
        print(str(resultitem) + ": " + df['product'][resultitem])
    print()
    print("Type in the index (number) of your requested item: ")
    requestitem = int(input())
    Walmart(df['sku'][requestitem],ZIP)
    return()



def Target(SKU, ZIP):
    SKU=str(SKU)
    if '-' not in SKU:
        SKU = ('{}-{}-{}'.format(SKU[0:3], SKU[3:5], SKU[5:9]))
    url = 'https://brickseek.com/target-inventory-checker/'
    payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}

    r = requests.post(url, data=payload).text    # Make a POST request with data

    bs = BeautifulSoup(r, 'html.parser')
    print(" Store                Availability      Quantity ")
    j=0
    for tag in bs.find_all('div', class_='table__body'): 
        for i in range(10):
            #print(tag)
            m_Store = tag.findAll('strong', class_='address-location-name')
            m=str(m_Store)
            if i < m.count('/strong'):
                m_s= m_Store[i].get_text()
                m_add = tag.findAll('address',class_="address")
                m_Address = m_add[i].contents[0]      
                m_Availability = tag.findAll('span',class_="availability-status-indicator__text")
                m_a = m_Availability[i].get_text()
                m_q = 'Unknown'
                j=j+1
                print( m_s+"   "  +  m_Address   + "      " + m_a + "        " + m_q ) 
            else:break
                
query = True
while query == True:
    print("Which one you want to check: 1. Walmart  2.Target")
    answer = input()
    if answer == '1':
        print("Type in key word of your requested item: ")
        answer1=str(input())
        print("Type in zipcode of your searching area: ")
        ZIP=int(input())
        query = False
        WalmartKeywords(answer1,ZIP)
    elif answer == '2':
        print("Type in DCPI of your requested item (you can find DCPI on target.com): ")
        SKU=int(input())
        print("Type in zipcode of your searching area: ")
        ZIP=int(input())
        query = False
        Target(SKU, ZIP)
    else: 
        print("Wrong input")