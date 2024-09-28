import stock_data

def buy(stock_name, ltp):
    balance_available = int(stock_data.get_balance())
    buy_list = stock_data.get_buy()
    buy_budget = balance_available / len(buy_list)
    print (buy_budget)
    quantity = int(buy_budget/ltp)
    if quantity > 0:
        stock_data.execute_buy(stock_name,quantity,ltp)
        new_balance = balance_available - (quantity * ltp)
        stock_data.update_balance(new_balance)
    print(f"{stock_name} is bought")

def sell(stock_name):
    sell_detail = stock_data.get_sell_details(stock_name)
    ltp = float(sell_detail[2])
    quantity = int(sell_detail[4])
    balance_available = float(stock_data.get_balance())
    stock_data.execute_sell(stock_name)
    new_balance = balance_available + (ltp * quantity)
    stock_data.update_balance(new_balance)
    print(f"{stock_name} is sold")

# buy('GPIL',939.15)