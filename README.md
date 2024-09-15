# algo-trading

## **Disclaimer:**
**Trading is subject to market risks, and Futures & Options (F&O) trading carries a high level of risk. I am not responsible for any financial losses or decisions made based on this project.**

## Overview:
This project involves a Python-based trading bot that automates scalping for BankNifty options. It integrates the Zerodha Kiteconnect API and TradingView to automate trading decisions and execution in real-time.

Key Features:

⦾ Real-Time Option Scalping: Executes trades for in-the-money (ITM) Nifty50 options based on predefined technical conditions.

⦾Zerodha KiteConnect API: Efficiently manages and executes trades using Zerodha’s API, ensuring smooth integration with the brokerage platform.

⦾TradingView Automation: Leverages real-time data from TradingView to generate signals for trade entry and exit.

⦾Predefined Strategy: Implements an algorithm with specific conditions such as price levels, option greeks, and time-based triggers to optimize trading decisions.

⦾Enhanced Responsiveness: Automates rapid decision-making and trade execution, reducing human errors and improving trading precision.

Modular Structure: 
Key files include:

⦾  enctoken.txt: Stores authentication tokens.

⦾  first_algo.py: Contains the main trading algorithm.

⦾  kc_option_contracts.py: Manages option contract details.

⦾  kiteapp.py: Integrates Kite API for trading actions.
