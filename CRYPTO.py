# Packages to import
from bs4 import BeautifulSoup
import requests
from csv import writer

# URL and user we want
url = 'https://www.coingecko.com/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

# Get a response from the website
page = requests.get(url, headers=headers)

# if the values of response are between 200-299 the page works propperly
# print(page)

# Parsing an html website and we want the content of it
soup = BeautifulSoup(page.content, "html.parser")

# Find all the values on the html
lists = soup.find_all('td', class_='coin-name') # must use underscore if not we have a python class

# Create a .csv file
with open('CYPTO.csv', 'w', encoding='utf8', newline='') as f:
	writer = writer(f)
	# Store in a list the values we want to extract from each currency and write them on the .csv file
	header = ['Currency', 'Price', 'Min 24h', 'Max 24h', 'All time high']
	writer.writerow(header)
	
	# Create 2 empty lists, one for the currency names and another for the currency names modified in order to access its html website
	list_coins = []
	list_coins_iterate = []
	
	# Iterate over all the coin names 
	for li in lists:
		# Obtain the name of the coin
		name = li.find('span', class_='lg:tw-flex font-bold tw-items-center tw-justify-between').text
		
		# Store the names of the crypto to iterate later changing every ' ' for a '-' and having all the letters lowercase
		name_good_iterate = ''
		for i in name:
			if i == "\n":
				empty = i
			elif i == ' ':
				name_good_iterate += '-'
			else:
				name_good_iterate += i.lower()
		
		list_coins_iterate.append(name_good_iterate)
		
		# Store the names of the Crypto
		name_good = ''
		for i in name:
			if i == "\n":
				empty = i
			else:
				name_good += i
		
		list_coins.append(name_good)

	# Iterate over the list of coins modified
	for coin_iterate in list_coins_iterate:
		
		# Obtain the all time high
		url_high = 'https://www.coingecko.com/en/coins/' + coin_iterate
		page_high = requests.get(url_high, headers=headers)
		soup_high = BeautifulSoup(page_high.content, "html.parser")
		
		# Check if the values are NoneType
		if soup_high.find('table', class_='table b-b') is None:
			discard = soup_high.find('table', class_='table b-b')
		else:
			table = soup_high.find('table', class_='table b-b')
		
		all_time = table.find_all('span', class_='no-wrap')[7].text # 7 as it is where our all time value is on the list

		# Obtain the remaining values
		url_coin = 'https://www.coingecko.com/en/coins/' + coin_iterate + '#markets'
		page_coin = requests.get(url_coin,headers=headers)
		
		soup = BeautifulSoup(page_coin.content, "html.parser")
		
		# Check if the prices are NoneType
		if soup.find('span', class_='no-wrap') is None:
			discard = soup.find('span', class_='no-wrap')
		else:	
			price = soup.find('span', class_='no-wrap').text
		
		# Check if the range is NoneType
		if soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1') is None:
			discard = soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1')
		
		else:
			range_left = soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1')
			range_prince_left = range_left.find('span', class_='no-wrap').text
		
		# Check if the range is NoneType
		if soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1 tw-text-right') is None:
			discard = soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1 tw-text-right')
		else:
			range_right = soup.find('div', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium tw-col-span-1 tw-text-right')
			range_price_right = range_right.find('span', class_='no-wrap').text
		
		# Store all the information in a list
		info = [list_coins[index], price, range_prince_left, range_price_right, all_time]
		# Write on the .cvs file the list
		writer.writerow(info)
		
