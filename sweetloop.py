from decide import Decide
import stock_data
import execute_order
import datetime
import pytz

def Status():
    time_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    hour_now = int(time_now.strftime("%H"))
    print(time_now.strftime("%H : %M : %S"))
    manual_stop = int(stock_data.check_manual_stop())
    if manual_stop == 1:
        return ["Manual Stop Engaged", False]

    else:
        if manual_stop == 2:
            return ["Error while executing buy", False]

        if manual_stop == 3:
            return ["Error while executing Sell", False]

        else:
            if hour_now < 10:
                return ["Waiting to open", False]

            if hour_now > 15:
                return ["Market closed", False]

            else:
                return ["Active", True]


def loop_operation():
    #Get a list of all the stocks from Database
    buy_list = stock_data.get_buy()
    drift = stock_data.drift_value()
    buy_ratio = stock_data.get_ratio('buy')
    for stock in buy_list:
        print(f"CHECK BUY : {stock}")
        buy_decision = Decide.buy(stock, drift, buy_ratio)
        stock_data.update_db('BUY_TABLE',stock,buy_decision[2],buy_decision[1])
        stock_data.update_buy_ratio(stock,buy_decision[3])
        if buy_decision[0] == True:
            execute_order.buy(stock, buy_decision[2])
            print(f"{stock} is bought")

    sell_list = stock_data.get_sell()
    gain = stock_data.gain_value()
    sell_ratio = stock_data.get_ratio('sell')
    for stock in sell_list:
        print(f"CHECK SELL : {stock}")
        buy_price = stock_data.buy_price(stock)
        sell_decision =  Decide.sell(stock,buy_price, gain, sell_ratio)
        stock_data.update_db('SELL_TABLE',stock,sell_decision[2],sell_decision[1])
        if sell_decision[0] == True:
            execute_order.sell(stock)
            print(f"{stock} is sold")

def add_stock(stock_name):
    buy_list = stock_data.get_buy()
    if stock_name not in buy_list:
        sell_list = stock_data.get_sell()
        if stock_name not in sell_list:
            stock_data.insert_stock(stock_name)

def remove_stock(stock_name):
    sell_list = stock_data.get_sell()
    if stock_name in sell_list:
        execute_order.sell(stock_name)
        stock_data.remove_stock(stock_name)

    else:
        buy_list = stock_data.get_buy()
        if stock_name in buy_list:
            stock_data.remove_stock(stock_name)

    print(f"{stock_name} is removed")

def manual_buy(stock_name):
    if stock_name in stock_data.get_buy():
        ltp = Decide.buy(stock_name,90,10)[2]
        if ltp != 0:
            execute_order.buy(stock_name,ltp)

def manual_sell(stock_name):
    if stock_name in stock_data.get_sell():
        execute_order.sell(stock_name)


def update_config(feed_list):
    if feed_list[0] != '':
        stock_data.update_config('DRIFT', feed_list[0])

    if feed_list[1] != '':
        stock_data.update_config('GAIN', feed_list[1])

    if feed_list[2] != '':
        stock_data.update_config('BUY_AT_RATIO', feed_list[2])

    if feed_list[3] != '':
        stock_data.update_config('SELL_AT_RATIO', feed_list[3])


# manual_buy('GPIL')
loop_operation()