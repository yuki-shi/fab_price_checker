from bs4 import BeautifulSoup
import pandas as pd	
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

class FaBuki():
	def __init__(self):
		self.driver = self.init_driver()

	def init_driver(self) -> webdriver:
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		driver = webdriver.Chrome(options=options)
		return driver	

	def card_search(self, card_name: str) -> pd.DataFrame:
		if ' ' in card_name:
		  card_name = re.sub(' ', '_', card_name)
		  print(card_name)

		self.driver.get(f'https://www.tcgplayer.com/search/flesh-and-blood-tcg/product?Language=English&productLineName=flesh-and-blood-tcg&q={card_name}&view=grid')
		
		sleep (5)
		
		html = self.driver.page_source
		
		soup = BeautifulSoup(html, 'html.parser')
		products = soup.find_all('div', class_='search-result')

		product_link = []
		product_col = []
		product_name = []

		for product in products:
		  for hyperlink in product.find_all('a', href=True):
		    product_link.append(hyperlink['href'])
		  for collection in product.find_all('h4'):
		    product_col.append(collection.text)
		  for name in product.find_all('span', class_='search-result__title'):
		    product_name.append(name.text)

		df = pd.DataFrame([product_link, product_col, product_name]).transpose()
		df = df.rename(columns={0: 'link',
				        1: 'collection',
				        2: 'card'})

		df['link'] = [f'https://www.tcgplayer.com{x}' for x in df['link']]
		return df

def scrape_tcgplayer() -> str:
	# Browser init
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	browser = webdriver.Chrome(options=options)

	# TODO: query word

	# Get URL
	#https://www.tcgplayer.com/search/flesh-and-blood-tcg/product?productLineName=flesh-and-blood-tcg&q=snatch+(red)&view=grid
	
	self.driver.get('https://www.tcgplayer.com/product/502719/flesh-and-blood-tcg-dusk-till-dawn-star-struck?xid=a12ed4db2-b3d8-4443-a813-85241a960a81&Language=English')

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
	fabuki = FaBuki()
	df = fabuki.card_search('snatch')
	print(df)        
