#!/Users/riley/Code/pythonprojects/PMC_Data/pmcdata-env/bin/python3

import numpy as np
import pandas as pd
import requests
import csv
import json


#VARIABLES REQUIRED FOR ETHERSCAN API REQUEST/DATAFRAME UPDATE/GOLD PRICING
ETHERSCAN_API_KEY = '{insert your own etherscan api key}'
GOLD_API_KEY = '{Insert your own api key }' #I got mine from metals-api.com , the free version only gives you 50 calls per month.
PMC_CONTRACT = '0x3A2e5440Ae3c621987f0eB75DE464455fC3F7AF7' #Public contract for PMC Coin
GWEI_MULTIPLIER = 1000000000000000000 # The number reaturned by the Ethercan API needs to be divided by this number
ADDRESS = ''
WALLET_BALANCE = 0
TOTAL = 0
SPOT_PRICE = 0
PMC_PRICE = 0
EXPECTED_HOLDINGS_USD = 0
EXPECTED_HOLDINGS_OZ = 0
    
#READ CSV FILE - CREATE DATAFRAME.
df = pd.read_csv(" 'example.csv' ",delimiter=',',index_col=False) #Using a CSV file was fine in my case, the number of wallets doesn't increase frequently.
df.insert(2,'Tokens',0) #Add another column called 'Tokens' to dataframe

#ITERATE THROUGH ROWS => GET RESPONSE,UPDATE DATAFRAME ROW WITH WALLET BALANCE
for column, row in df.iterrows():
    ADDRESS = df.loc[column,'Wallet']
    response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + PMC_CONTRACT + "&address=" + ADDRESS + "&tag=latest&apikey=" + ETHERSCAN_API_KEY)
    WALLET_BALANCE = float(response.json()['result']) / GWEI_MULTIPLIER
    df.loc[column,'Tokens'] = WALLET_BALANCE

    TOTAL = TOTAL + WALLET_BALANCE
    print("Getting balance for " + df.loc[column,'Name'])

#GET GOLD SPOT PRICE VIA METALS-API.COM AND CALCULATE EXPECTED HOLDINGS AND PMC PRICE
response = requests.get("http://metals-api.com/api/latest?access_key=" + GOLD_API_KEY + "&base=USD&symbols=XAU")
xau_value = float(response.json()['rates']['XAU'])
SPOT_PRICE = 1/xau_value
PMC_PRICE = SPOT_PRICE/50
EXPECTED_HOLDINGS_USD = TOTAL * PMC_PRICE
EXPECTED_HOLDINGS_OZ = EXPECTED_HOLDINGS_USD / SPOT_PRICE

#SORT AND PRINT DATAFRAME
df.sort_values(by=['Tokens'],inplace=True, ascending=False)

print(df)
print("\nThe PMC balance of all known wallets is " + str(TOTAL))
print("\nThe Gold Spot Price is " + str("${:,.2f}".format(SPOT_PRICE)))
print("\nExpected Gold holdings in USD is " + str("${:,.2f}".format(EXPECTED_HOLDINGS_USD)))
print("\nExpected Gold holdings in OUNCES is " + str(EXPECTED_HOLDINGS_OZ) + "\n") 
    

    
    


