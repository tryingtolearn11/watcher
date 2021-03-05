from pycoingecko import CoinGeckoAPI
from app import app


# TODO: Display data to html
#       Attach to Database

cg = CoinGeckoAPI()



def test():
    data = cg.get_price(ids='bitcoin', vs_currencies='usd')
    print(data)

print(test())
