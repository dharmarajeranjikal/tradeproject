import sqlite3

db_name = 'stock_data.db'

def get_buy():
    #This function return a list of stock names in to_buy table
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM BUY_TABLE")
    db_output = cursor.fetchall()
    connection.close()
    # print(db_output)
    result = []
    for data in db_output:
        # print(data[0])
        result.append(data[0])
    return result

def get_sell():
    #This function returns a list of stock names in to_sell table
    # return ['NCC','NBCC']
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SELL_TABLE")
    db_output = cursor.fetchall()
    connection.close()
    # print(db_output)
    result = []
    for data in db_output:
        # print(data[0])
        result.append(data[0])
    return result

def get_display(table_name):
    #This function returns a dictionary with stock data
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT * FROM {table_name}""")
    db_output = cursor.fetchall()
    connection.close()
    return db_output


def drift_value():
    #This function returns the % at which we buy when market drops
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT VALUE FROM CONFIG WHERE PARTICULAR = 'DRIFT'")
    db_output = cursor.fetchall()
    connection.close()
    return int(db_output[0][0])

def gain_value():
    #This function return at what % of gain the stock must be sold
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT VALUE FROM CONFIG WHERE PARTICULAR = 'GAIN'")
    db_output = cursor.fetchall()
    connection.close()
    return int(db_output[0][0])

def get_balance():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT VALUE FROM CONFIG WHERE PARTICULAR = 'BALANCE_AMOUNT'")
    db_output = cursor.fetchall()
    connection.close()
    return float(db_output[0][0])

def update_balance(new_value):
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
        UPDATE CONFIG SET VALUE = '{new_value}'
        WHERE PARTICULAR = 'BALANCE_AMOUNT'
         """)
    connection.commit()
    connection.close()

def update_buy_ratio(stock_name, ratio):
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
        UPDATE BUY_TABLE SET BUY_RATIO = '{ratio}'
        WHERE STOCK = '{stock_name}'
         """)
    connection.commit()
    connection.close()

def buy_price(stock_name):
    #this function returns the price at which the stock is bought
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT BUY_PRICE FROM SELL_TABLE WHERE STOCK='{stock_name}'")
    db_output = cursor.fetchall()
    connection.close()
    return float(db_output[0][0])

def update_db(table_name, stock_name, ltp, flag_number):
    #this function shall update the ltp value in database
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
    UPDATE {table_name} SET LTP = '{ltp}', FLAG ='{flag_number}'
    WHERE STOCK = '{stock_name}'
     """)
    connection.commit()
    connection.close()

def execute_buy(stock_name, quantity, bought_price):
    #This function removes stock details from BUY_LIST and  inserts into SELL_LIST
    connection = sqlite3.connect(db_name)
    connection.execute(f""" 
    DELETE FROM BUY_TABLE WHERE STOCK = '{stock_name}'""")
    connection.commit()

    connection.execute(f"""
    INSERT INTO SELL_TABLE (STOCK,BUY_PRICE,LTP,FLAG,QTY) 
    VALUES ('{stock_name}','{bought_price}',{bought_price},'0','{quantity}')
     """)
    connection.commit()
    connection.close()

def execute_sell(stock_name):
    connection = sqlite3.connect(db_name)
    connection.execute(f""" 
    DELETE FROM SELL_TABLE WHERE STOCK = '{stock_name}'""")
    connection.commit()

    connection.execute(f"""
    INSERT INTO BUY_TABLE (STOCK) VALUES ('{stock_name}')
     """)
    connection.commit()
    connection.close()

def get_sell_details(stock_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"""
            SELECT * FROM SELL_TABLE WHERE STOCK = '{stock_name}'
            """)
    result = cursor.fetchall()
    connection.close()
    return result[0]

def check_manual_stop():
    #This fucntions returns the Manual Stop flag from database
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT VALUE FROM CONFIG WHERE PARTICULAR = 'MANUAL_STOP'")
    db_output = cursor.fetchall()
    connection.close()
    return int(db_output[0][0])

def set_manual_stop():
    #This function is used to set manual stop in the database inorder to stop the program
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
    UPDATE CONFIG SET VALUE = '1' WHERE PARTICULAR = 'MANUAL_STOP'
     """)
    connection.commit()
    connection.close()

def raise_error_code(code_number):
    #This function is used to set manual stop in the database inorder to stop the program
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
    UPDATE CONFIG SET VALUE = '{code_number}' WHERE PARTICULAR = 'MANUAL_STOP'
     """)
    connection.commit()
    connection.close()

def get_summary_data():
    #This returns data to be displayed int he summary block of the UI
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(BUY_PRICE) FROM SELL_TABLE")
    db_output = cursor.fetchall()
    if db_output[0][0] != None:
        sum_buy_price = float(db_output[0][0])

    else:
        sum_buy_price = 0

    cursor.execute("SELECT SUM(LTP) FROM SELL_TABLE")
    db_output = cursor.fetchall()
    if db_output[0][0] != None:
        sum_current_value = float(db_output[0][0])

    else:
        sum_current_value = 0
    connection.close()

    gain = sum_current_value - sum_buy_price

    return [sum_current_value, sum_buy_price, round(gain,2)]

def insert_stock(stock_name):
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
    INSERT INTO BUY_TABLE (STOCK,LTP,FLAG,BUY_RATIO) 
    VALUES ('{stock_name}','0','0','0')
     """)
    connection.commit()
    connection.close()

def remove_stock(stock_name):
    connection = sqlite3.connect(db_name)
    connection.execute(f""" 
    DELETE FROM BUY_TABLE WHERE STOCK = '{stock_name}'""")
    connection.commit()
    connection.close()

def update_config(field_name, value):
    #This fuction is used to update buy and sell ratio values in db
    connection = sqlite3.connect(db_name)
    connection.execute(f"""
    UPDATE CONFIG SET VALUE = '{value}' WHERE PARTICULAR = '{field_name}'
     """)
    connection.commit()
    connection.close()

def get_ratio(type):
    #Returns buy and sell ratio values from db
    field_name =''
    if type == 'buy':
        field_name = 'BUY_AT_RATIO'

    if type == 'sell':
        field_name = 'SELL_AT_RATIO'

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT VALUE FROM CONFIG WHERE PARTICULAR = '{field_name}'")
    db_output = cursor.fetchall()
    connection.close()
    return int(db_output[0][0])


main_op = get_ratio('sell')
print(main_op)
# set_manual_stop()
# insert_stock("JSWSTEEL")
# raise_error_code(2)