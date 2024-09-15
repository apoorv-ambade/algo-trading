import kiteapp as kt
import datetime
import kc_option_contracts as opt_chain
import pandas as pd
import datetime as dt
import time

#1
#token = unique enc token
with open('enctoken.txt', 'r') as wr:
    token = wr.read()

kite = kt.KiteApp("User name here", "Zerodha user ID here", token)

print(kite.ohlc("NSE:NIFTY BANK"))



#time loop
start_time = datetime.time(9, 17)
end_time = datetime.time(15, 15)

#global variables
win_count = 6
lock = "false"

time.sleep(60 - (dt.datetime.now().second))

while True:
    current_time = datetime.datetime.now().time()
    if current_time >= start_time and current_time <= end_time:
        #print("*** Market Open ***")

        #2
        itm_call = opt_chain.option_contracts_itm_CE("BANKNIFTY",kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"], 0)
        itm_put = opt_chain.option_contracts_itm_PE("BANKNIFTY",kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"], 0)

        symbol_CE = (itm_call["tradingsymbol"])
        symbol_PE = (itm_put["tradingsymbol"])

       # print(symbol_CE)
        #print(symbol_PE)

        #3

        to_date = dt.datetime.now().date()
        from_date = to_date - dt.timedelta(days=1)

        df = kite.historical_data(instrument_token=260105, from_date=from_date, to_date=to_date, interval='minute',
                                  oi=True)
        df = pd.DataFrame(df)

        candle_1_colour = "NULL"
        candle_2_colour = "NULL"

        #4
        if (dt.datetime.now().second < 30):
            last_two_rows = df.tail(2)

            # Extracting values into variables item1 and item2
            candle_1 = last_two_rows.iloc[0]  # Extracting the last but one row
            candle_2 = last_two_rows.iloc[1]  # Extracting the last row

        else:
            candle_1 = df.iloc[-3]  # Extracting the last but one row
            candle_2 = df.iloc[-2]

        if (candle_1["open"] >= candle_1["close"]):
            candle_1_colour = "red"
        else:
            candle_1_colour = "green"

        if (candle_2["open"] >= candle_2["close"]):
            candle_2_colour = "red"
        else:
            candle_2_colour = "green"

        H1 = max(candle_1["high"], candle_2["high"])  # HIGH
        L1 = min(candle_1["low"], candle_2["low"])  # LOW


        # print("seconds:"+str(dt.datetime.now().second))
        # print(H1)
        # print(L1)
        # print(kite.ltp("NSE:NIFTY BANK"))

        #5
        # BUY CE
        price = kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"]
        # declare lock as global variable (clock loop ke bahar)
        # declare win count also as global variable


        if ('''Buy CE condition here'''):

            #if buy successful, then set locks... else repeat
            print("BUY CE")

            lock = "true"
            x = 0
            BNF_execution_price = price

            ''' Place buy order code below '''
            oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_CE,
                                   transaction_type="BUY", quantity=15, product="MIS", order_type="MARKET",
                                   validity="DAY")
            order_id = oid
            # Fetch order details using order ID
            order_info = kite.order_history(order_id)
            # Retrieve the execution price from order details

            order_history = kite.order_history(oid)
            latest_row_index = len(order_history) - 1
            execution_price = order_info[latest_row_index]["average_price"]

            # TRAILING STOP LOSS
            set_point = execution_price + 5
            stop_loss = execution_price + 1
            trailing_stop_loss = 5

            print("WIN COUNT" + str(win_count + 1))

            #  order_status="INCOMPLETE"
            if win_count >= 4:

                print("TSL CE")
                # EXCEPTION: Stoploss Market orders (SL-M) are blocked for F&O contracts as they have been discontinued by the exchange.
                # Use SL Limit orders instead.

                sl_order_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_CE,
                                                transaction_type="SELL", quantity=15, product="MIS", order_type="SL",
                                                trigger_price=(execution_price - 3),price=(execution_price - 3.25), validity="DAY")


                order_status = "NULL"

                while (order_status != "COMPLETE"):


                    order_history=kite.order_history(sl_order_oid)
                    latest_row_index = len(order_history) - 1
                    order_status = kite.order_history(sl_order_oid)[latest_row_index]['status']
                    if (kite.order_history(sl_order_oid)[latest_row_index]['status'] == "COMPLETE"):
                        break

                    if ('''trailing Stop loss order below'''):
                        win_count = win_count + 1

                        sl_order_oid = kite.modify_order(order_id=sl_order_oid, variety="regular",  quantity=15,
                                                         order_type="SL", trigger_price=stop_loss, price=(stop_loss - 0.50), validity="DAY")

                        stop_loss = stop_loss + trailing_stop_loss
                        set_point = set_point + trailing_stop_loss

                lock = "false"

                time.sleep(61 - (dt.datetime.now().second))

                # sleep(until candle closes)


            else:

                print("SAFE CE")
                ''' Sell order below'''
                take_profit_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_CE,
                                                   transaction_type="SELL", quantity=15, product="MIS",
                                                   order_type="LIMIT",
                                                   price=(execution_price + 2), validity="DAY")

                # while loop se if BNF_execution_price - ltp < 4 then SL market.
                # set lock
                while x != 1:
                    if ('''stop loss order below'''):
                        kite.cancel_order("regular", take_profit_oid)
                        take_SL_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_CE,
                                                       transaction_type="SELL", quantity=15, product="MIS",
                                                       order_type="LIMIT", price=(execution_price - 2.25),
                                                       validity="day")

                        # write code to cancel take_profit order (as it will not automatically cancel) (Done above)
                        print("book loss")
                        win_count = win_count - 1
                        lock = "false"
                        x = 1


                    order_history=kite.order_history(take_profit_oid)
                    latest_row_index = len(order_history) - 1
                    if (kite.order_history(take_profit_oid)[latest_row_index]['status'] == "COMPLETE"):
                        print("book profit")
                        win_count = win_count + 1
                        lock = "false"
                        x = 1

                time.sleep(61 - (dt.datetime.now().second))

            # Sleep(until candle closes)
            # place buy CE order
            # place stop loss market order
            # place take profit limit order

        # BUY PE
        if ('''Buy PE condition here'''):

            print("BUY PE")

            lock = "true"
            x = 0
            BNF_execution_price = price

            oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_PE,
                                   transaction_type="BUY", quantity=15, product="MIS", order_type="MARKET",
                                   validity="DAY")

            order_id = oid
            # Fetch order details using order ID
            order_info = kite.order_history(order_id)
            # Retrieve the execution price from order details

            order_history = kite.order_history(oid)
            latest_row_index = len(order_history) - 1
            execution_price = order_info[latest_row_index]["average_price"]

            # Trailing Stop Loss
            set_point = execution_price + 5
            stop_loss = execution_price + 1
            trailing_stop_loss = 5

            print("WIN COUNT" + str(win_count + 1))

            if win_count >= 4:

                print("TSL PE")

                sl_order_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_PE,
                                                transaction_type="SELL", quantity=15, product="MIS", order_type="SL",
                                                trigger_price=(execution_price - 3),price=(execution_price - 3.25), validity="DAY")

                order_status = "NULL"

                while (order_status != "COMPLETE"):

                    order_history=kite.order_history(sl_order_oid)
                    latest_row_index = len(order_history) - 1
                    order_status = kite.order_history(sl_order_oid)[latest_row_index]['status']

                    if (kite.order_history(sl_order_oid)[latest_row_index]['status'] == "COMPLETE"):
                        break

                    if ('''Trailing stop loss here'''):
                        win_count = win_count + 1

                        sl_order_oid = kite.modify_order(order_id=sl_order_oid, variety="regular", quantity=15,
                                                         order_type="SL", trigger_price=stop_loss,price=(stop_loss- 0.50), validity="DAY")

                        stop_loss = stop_loss + trailing_stop_loss
                        set_point = set_point + trailing_stop_loss

                lock = "false"
                time.sleep(61 - (dt.datetime.now().second))

            else:

                print("SAFE PE")
                take_profit_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_PE,
                                                   transaction_type="SELL", quantity=15, product="MIS",
                                                   order_type="LIMIT",
                                                   price=(execution_price + 2), validity="DAY")

                while x != 1:
                    if ('''Stop loss order below'''):
                        kite.cancel_order("regular", take_profit_oid)
                        take_SL_oid = kite.place_order(variety="regular", exchange="NFO", tradingsymbol=symbol_CE,
                                                       transaction_type="SELL", quantity=15, product="MIS",
                                                       order_type="LIMIT", price=(execution_price - 2.25),
                                                       validity="day")
                        print("Book loss")
                        win_count = win_count - 1
                        lock = "false"
                        x = 1

                    order_history=kite.order_history(take_profit_oid)
                    latest_row_index = len(order_history) - 1
                    if (kite.order_history(take_profit_oid)[latest_row_index]['status'] == "COMPLETE"):
                        print("Book profit")
                        win_count = win_count + 1
                        lock = "false"
                        x = 1

                time.sleep(61 - (dt.datetime.now().second))

        print("1st block successful")


    else:
        print("*** Market Closed ***")
        exit(1)
