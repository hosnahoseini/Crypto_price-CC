from fastapi import FastAPI
from pycoingecko import CoinGeckoAPI
from redis import Redis
import uvicorn
import os
import configparser
import requests

config = configparser.ConfigParser()
config.read('/app/config.ini')

app = FastAPI()
cg = CoinGeckoAPI()
r = Redis(host=config['DEFAULT']['REDIS_HOST'],
          port=config['DEFAULT']['REDIS_PORT'],
          password=os.environ['REDIS_PASSWORD'])

exp_time = int(config['DEFAULT']['EXP_TIME'])
crypto_name = config['DEFAULT']['CRYPTO_NAME']

@app.get("/flush_cache")
async def flush():
    r.flushdb()

@app.get("/crypto")
async def root():
    description = ''
    if (r.exists(crypto_name)):
        description = 'result from redis'
        result = r.get(crypto_name).decode('ascii')

    else:
        description = 'result from api'
        url = f'https://rest.coinapi.io/v1/exchangerate/{crypto_name}/USD'
        headers = {'X-CoinAPI-Key' : config['DEFAULT']['API_KEY']}
        result = requests.get(url, headers=headers).json()["rate"]
        r.mset({crypto_name: result})
        r.expire(crypto_name, exp_time)


    return {"crypto name": crypto_name, "price": str(result), "description": description}
            
if __name__ == "__main__":          
    uvicorn.run("main:app", host="0.0.0.0", port=int(config['DEFAULT']['PROJ_PORT']))