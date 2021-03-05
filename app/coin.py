from pycoingecko import CoinGeckoAPI
# from app import app


cg = CoinGeckoAPI()



def test():
    data = cg.get_price(ids='bitcoin', vs_currencies='usd')
    print(data)

print(test())
