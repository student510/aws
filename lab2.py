import boto3
import requests
import matplotlib.pyplot as plt
import pandas as pd
from json import loads

usd_link = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=asc&json'
eur_link = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=asc&json'

usd = requests.get(usd_link).json()
eur = requests.get(eur_link).json()

data_usd = []
data_eur = []

for i in usd:
    data_usd.append({'date': i['exchangedate'], 'USD': i['rate']})
for i in eur:
    data_eur.append({'date': i['exchangedate'], 'EUR': i['rate']})

df_usd = pd.DataFrame(data_usd).set_index('date')
df_eur = pd.DataFrame(data_eur).set_index('date')

data = pd.concat([df_usd, df_eur], axis=1)
data.to_csv('rate.csv')

bucket = boto3.client('s3')

bucket.upload_file('rate.csv', 'frogdata', 'rate.csv')

bucket.download_file('frogdata', 'rate.csv', 'rate.csv')
viz = pd.read_csv('rate.csv', sep=',')
viz.plot(x='date', y=['USD', 'EUR'], figsize=(16, 8), title="UAH", fontsize=12)

plt.savefig('rate.png')

bucket.upload_file('rate.png', 'frogdata', 'rate.png')
