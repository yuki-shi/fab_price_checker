import requests
import json

class FaBuki():
  def __init__(self):
    self.headers = {
        'authority': 'mp-search-api.tcgplayer.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'referer': 'https://www.tcgplayer.com/',
        'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    self.json_data = {
        'algorithm': 'sales_exp_fields_experiment',
        'from': 0,
        'size': 24,
        'filters': {
            'term': {
                'productLineName': [
                    'flesh-and-blood-tcg',
                ],
            },
            'range': {},
            'match': {},
        },
        'listingSearch': {
            'context': {
                'cart': {},
            },
            'filters': {
                'term': {
                    'sellerStatus': 'Live',
                    'channelId': 0,
                    'language': [
                        'English',
                    ],
                },
                'range': {
                    'quantity': {
                        'gte': 1,
                    },
                },
                'exclude': {
                    'channelExclusion': 0,
                },
            },
        },
        'context': {
            'cart': {},
            'shippingCountry': 'BR',
        },
        'settings': {
            'useFuzzySearch': True,
            'didYouMean': {},
        },
        'sort': {},
    }

  def card_search(self, card_name: str):
      params = {
        'q': card_name,
        'isList': 'false',
        'mpfev': '1953',
      }

      response = requests.post(
          'https://mp-search-api.tcgplayer.com/v1/search/request',
          params=params,
          headers=self.headers,
          json=self.json_data,
      )

      response_json = json.loads(response.text)
      plp = response_json['results'][0]['results']

      products = []

      for product in plp:
        products.append([product['productName'], product['setName'], int(product['productId'])])

      return products

  def check_latest_sales(self, product_id: str):
      params = {
      'mpfev': '1953',
      }

      response = requests.post(
          f'https://mpapi.tcgplayer.com/v2/product/{product_id}/latestsales',
          params=params,
          headers=self.headers,
          json={},
      )

      response_json = json.loads(response.text)

      latest_sales = []

      sales = response_json['data']

      for sale in sales:
        latest_sales.append([sale['condition'], sale['variant'], sale['title'], sale['quantity'], sale['purchasePrice']])

      return latest_sales
