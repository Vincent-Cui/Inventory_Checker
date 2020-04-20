import streamlit as st
import requests
import bs4
from lxml import html
from bs4 import BeautifulSoup
from distutils.filelist import findall
import requests
import re
import pandas as pd
from utils import cache_on_button_press

@cache_on_button_press('Search')
def WalmartKeywords(keywords):
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
		st.write(str(resultitem) + ": " + df['product'][resultitem])
	return df


@cache_on_button_press('Confirm')
def Walmart(requestitem, ZIP):
	SKU=DF['sku'][int(requestitem)]
	url = 'https://brickseek.com/walmart-inventory-checker/'
	payload = {'search_method': 'sku', 'sku': SKU, 'zip': ZIP, 'sort': 'distance'}
	df_record = pd.DataFrame(columns=['Store','City','Availability','Quantity'])
	r = requests.post(url, data=payload).text    # Make a POST request with data
	
	bs = BeautifulSoup(r, 'html.parser')
	j=0
	a = bs.find_all('div', class_='table__body')
	if a == []:
		st.write('No results found in the searched area.')
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
					st.table(df_record)
					if len(df_record) == 0:
						st.write("No result found")
					break



@cache_on_button_press('Search')
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
	event_list=['Walmart','Target']
	event_type = st.sidebar.selectbox(
	'Which one you want to check: ',
	event_list
)

	if event_type == 'Walmart':
		kw=st.text_input("Type in key word of your requested item: ")
		DF = WalmartKeywords(str(kw))
		requestitem = st.number_input("Type in the index (number) of your requested item: ",0,100,1)
		ZIP=st.number_input("Type in zipcode of your searching area: ",0,100000,1)
		Walmart(requestitem, int(ZIP))
		query = False
	elif event_type == 'Target':
		SKU=st.number_input("Type in DCPI of your requested item (you can find DCPI on target.com): ",1)
		ZIP=st.number_input("Type in zipcode of your searching area: ",1)
		query = False
		Target(SKU, int(ZIP))
	else: 
		print("Wrong input")
st.markdown("""
Thank you for using Inventory Checker Version: 0.2

Released on: 19/04/2020

Source code is available at: https://github.com/Vincent-Cui/Inventory_Checker

Development Team: Wencong(Vincent) Cui, Jinwen Xu'
""")