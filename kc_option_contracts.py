# -*- coding: utf-8 -*-
"""
Zerodha Kite Connect - Option chain

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""
from kiteconnect import KiteConnect
import os
import datetime as dt
import yfinance as yf
import numpy as np
import pandas as pd

# cwd = os.chdir("D:\\OneDrive\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")
#
# #generate trading session
# access_token = open("access_token.txt",'r').read()
# key_secret = open("api_key.txt",'r').read().split()
# kite = KiteConnect(api_key=key_secret[0])
# kite.set_access_token(access_token)

import kiteapp as kt
import pandas as pd
import datetime as dt

with open('enctoken.txt', 'r') as wr:
    token = wr.read()

kite = kt.KiteApp("Apoorv", "LAD430", token)


#get dump of all NFO instruments
instrument_list = kite.instruments("NFO")

def option_contracts_CE(ticker, option_type="CE", exchange="NFO"):
    option_contracts = []
    for instrument in instrument_list:
        if instrument["name"]==ticker and instrument["instrument_type"]==option_type:
            option_contracts.append(instrument)
    return pd.DataFrame(option_contracts)

def option_contracts_PE(ticker, option_type="PE", exchange="NFO"):
    option_contracts = []
    for instrument in instrument_list:
        if instrument["name"]==ticker and instrument["instrument_type"]==option_type:
            option_contracts.append(instrument)
    return pd.DataFrame(option_contracts)
        
#df_opt_contracts = option_contracts_CE("BANKNIFTY")

#function to extract the closest expiring option contracts
def option_contracts_closest_CE(ticker, duration = 0, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_CE(ticker)
    df_opt_contracts["time_to_expiry"] = (pd.to_datetime(df_opt_contracts["expiry"]) - dt.datetime.now()).dt.days
    min_day_count = np.sort(df_opt_contracts["time_to_expiry"].unique())[duration]
    
    return (df_opt_contracts[df_opt_contracts["time_to_expiry"] == min_day_count]).reset_index(drop=True)


def option_contracts_closest_PE(ticker, duration=0, option_type="CE", exchange="NFO"):
    # duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_PE(ticker)
    df_opt_contracts["time_to_expiry"] = (pd.to_datetime(df_opt_contracts["expiry"]) - dt.datetime.now()).dt.days
    min_day_count = np.sort(df_opt_contracts["time_to_expiry"].unique())[duration]

    return (df_opt_contracts[df_opt_contracts["time_to_expiry"] == min_day_count]).reset_index(drop=True)


#df_opt_contracts = option_contracts_closest_CE("BANKNIFTY", 1)

#function to extract closest strike options to the underlying price
hist_data = yf.download("^NSEBANK", period='5d')
underlying_price = hist_data["Adj Close"].iloc[-1]

def option_contracts_atm(ticker, underlying_price, duration = 0, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_closest_CE(ticker, duration)
    return df_opt_contracts.iloc[abs(df_opt_contracts["strike"] - underlying_price ).argmin()]

def option_contracts_itm_CE(ticker, underlying_price, duration = 0, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_closest_CE(ticker, duration)
    return df_opt_contracts.iloc[abs(df_opt_contracts["strike"] - underlying_price +100 ).argmin()]

def option_contracts_itm_PE(ticker, underlying_price, duration = 0, option_type="PE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_closest_PE(ticker, duration)
    return df_opt_contracts.iloc[abs(df_opt_contracts["strike"] - underlying_price +50  ).argmin()]

atm_contract = option_contracts_atm("BANKNIFTY",underlying_price, 0)

itm_contract_CE = option_contracts_itm_CE("BANKNIFTY", underlying_price, 0)
itm_contract_PE = option_contracts_itm_PE("BANKNIFTY", underlying_price, 0)


#function to extract n closest options to the underlying price
def option_chain(ticker, underlying_price, duration = 0, num = 5, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    #num =5 means return 5 option contracts closest to the market
    df_opt_contracts = option_contracts_closest_CE(ticker, duration)
    df_opt_contracts.sort_values(by=["strike"],inplace=True, ignore_index=True)
    atm_idx = abs(df_opt_contracts["strike"] - underlying_price).argmin()
    up = int(num/2)
    dn = num - up
    return df_opt_contracts.iloc[atm_idx-up:atm_idx+dn]

opt_chain = option_chain("BANKNIFTY", underlying_price, 0)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#print(atm_contract)
#print(itm_contract_CE)
# print("\n")
#print(itm_contract_PE)


#print (option_chain("BANKNIFTY", underlying_price, duration = 0, num = 5, option_type="CE", exchange="NFO"))

#print(kite.ltp("NSE:BANKNIFTY"))
