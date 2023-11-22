from bs4 import BeautifulSoup
import pandas as pd	
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

def scrape_tcgplayer() -> str:
	# Browser init
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	browser = webdriver.Chrome(options=options)

	# TODO: query word

	# Get URL
	browser.get('https://www.tcgplayer.com/product/502719/flesh-and-blood-tcg-dusk-till-dawn-star-struck?xid=a12ed4db2-b3d8-4443-a813-85241a960a81&Language=English')

	# Wait until rendered TODO
	sleep(5)

	# Find sales history modal button and click it
	latest_sales = browser.find_element(By.XPATH,'//*[@id="app"]/div/div/section[2]/section/div/div[2]/section[3]/div/h3/div/div[1]')
	latest_sales.click()

	# Wait until rendered TODO
	sleep(5)

	html = browser.page_source
	
	return html

def format_to_dataframe(html: str) -> pd.DataFrame:
	soup = BeautifulSoup(html, 'html.parser')
	latest_sales = soup.find_all('section', class_='sales-history-snapshot__latest-sales')

	sales = []

	for sale in latest_sales:
	  for li in sale.find_all('li'):
	    sales.append(li.text)

	sales_details = []

	for sale in sales:
	  sale_split = sale.split()

	  qtd = re.findall(r'.*(?=\$)', sale_split[-1])[0]
	  price = re.findall(r'(?<=\$).*', sale_split[-1])[0]

	  sale_split = sale_split[:-1]
	  sale_split.extend([qtd, price])

	  sales_details.append(sale_split)

	for index, sale in enumerate(sales_details):
	  if len(sale) == 4:
	    sale.insert(2, 'NF')
	  else:
	    sale[2] = f'{sale[2]}-{sale[3]}'
	    sale.pop(3)

	df = pd.DataFrame(sales_details,
		          columns=['date',
		                    'condition',
		                    'foil',
		                    'qtd',
		                    'price'])
		                    
	df.loc[df['foil'] == 'Rainbow-Foil', 'foil'] = 'RF'
	df.loc[df['foil'] == 'Cold-Foil', 'foil'] = 'CF'	
	                   
	return df		      

if __name__ == '__main__':
	df = format_to_dataframe(scrape_tcgplayer())
	print(df.head())              
