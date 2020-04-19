'''

Inventory Checker for Walmart & Target

Author: Vincent Cui

'''


import requests
import bs4
from lxml import html
from bs4 import BeautifulSoup
from distutils.filelist import findall
def Walmart(SKU, ZIP):
    url = 'https://brickseek.com/walmart-inventory-checker/'
    payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}

    r = requests.post(url, data=payload).text    # Make a POST request with data


    bs = BeautifulSoup(r, 'html.parser')
    print(" Store                         City                       Availability      Quantity ")
    j=0
    for tag in bs.find_all('div', class_='table__body'): 
        for i in range(10):
            m_Store = tag.findAll('strong', class_='address-location-name')
            m_Store = tag.findAll('strong', class_='address-location-name')
            m=str(m_Store)
            if i < m.count('/strong'):
                m_s= m_Store[i].get_text()
                m_add = tag.findAll('address',class_="address")
                m_Address = m_add[i].contents[2]      
                m_Availability = tag.findAll('span',class_="availability-status-indicator__text")
                m_a = m_Availability[i].get_text()
                if m_a =='Out of Stock':
                    m_q = str(0)
                    j=j-1
                else:    
                    m_Quantity = tag.findAll('span',class_="table__cell-quantity")
                    m_q = m_Quantity[j].get_text()[9:]
                j=j+1
                print( m_s+"   "  +  m_Address   + "      " + m_a + "        " + m_q ) 
            else:break
            
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