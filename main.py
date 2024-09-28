import justpy as jp
import time
import asyncio
import sweetloop
import stock_data

#EVENET HANDLER--------------------------------------------------------
def add_stock_event(widget, msg):
    if widget.script_code.value != '':
        sweetloop.add_stock(widget.script_code.value)
        widget.script_code.value =''

def remove_stock_event(widget, msg):
    if widget.script_code.value != '':
        sweetloop.remove_stock(widget.script_code.value)
        widget.script_code.value =''

def manual_buy_event(widget, msg):
    if widget.script_code.value != '':
        sweetloop.manual_buy(widget.script_code.value)
        widget.script_code.value =''

def manual_sell_event(widget, msg):
    if widget.script_code.value != '':
        sweetloop.manual_sell(widget.script_code.value)
        widget.script_code.value =''

def manual_stop_event(widget, msg):
    stock_data.set_manual_stop()

def update_config(widget,msg):
    a = widget.drift.value
    b = widget.gain.value
    c = widget.ba_ratio.value
    d = widget.sa_ratio.value
    feed_list = [a,b,c,d]
    sweetloop.update_config(feed_list)
    widget.drift.value = ''
    widget.gain.value = ''
    widget.ba_ratio.value = ''
    widget.sa_ratio.value = ''

#_______________________________________________________________________
# UI BEGINS HERE _______________________________________________________

wp = jp.WebPage(delete_flag=False)

format_value = "font-medium text-base pt-3"
format_lable = "font-extralight text-xs"

clock_div = jp.Span(text='Loading...', classes=format_lable, a=wp)
page = jp.Div(a=wp, classes="bg-gray h-screen p-2")
status_block = jp.Div(a=page, text=f"Status : Booting up")

# SUMMARY BLOCK
summary_block = jp.Div(a=page, text="Summary", classes="rounded-md bg-white shadow-lg m-2 p-2 text-lg font-medium")
summary_grid = jp.Div(a=summary_block, classes="grid grid-cols-2")
total_value = jp.Div(a=summary_grid, text="unable to update", classes=format_value)
invested_value = jp.Div(a=summary_grid, text='unable to update', classes=format_value)
jp.Div(a=summary_grid, text="Current Value", classes=format_lable)
jp.Div(a=summary_grid, text="Current Investment", classes=format_lable)
gain_value = jp.Div(a=summary_grid, text="unable to update", classes=format_value)
balance_summary = jp.Div(a=summary_grid, text="unable to update", classes=format_value)
jp.Div(a=summary_grid, text="Gain/Loss", classes=format_lable)
jp.Div(a=summary_grid, text="Balance", classes=format_lable)

# HOLDING BLOCK
sell_card = jp.Div(a=page, text="Holdings", classes="rounded-md bg-white shadow-lg m-2 p-2 text-lg font-medium")
sell_display = jp.Div(a=sell_card)

# OPPORTUNITY BLOCK
buy_card = jp.Div(a=page, text="Opportunities", classes="rounded-md bg-white shadow-lg m-2 p-2 text-lg font-medium")
buy_display = jp.Div(a=buy_card)

# STTINGS BLOCK
settings_block = jp.Div(a=page, text="Configure", classes="rounded-md bg-white shadow-lg m-2 p-2 text-lg font-medium")
settings_grid = jp.Div(a=settings_block, classes="grid grid-cols-2")
# drift_display_value = jp.Div(a=settings_grid, text='Fetching ...', classes=format_value)
# gain_display_value = jp.Div(a=settings_grid, text='Fetching ...', classes=format_value)

drift_field = jp.Input(a=settings_grid, placeholdder='Fetching..',classes=format_value)
gain_field = jp.Input(a=settings_grid, placeholder='Fetching...', classes=format_value)
jp.Div(a=settings_grid, text="Drift Value", classes=format_lable)
jp.Div(a=settings_grid, text="Gain Margin", classes=format_lable)

buy_at_ratio = jp.Input(a=settings_grid, placeholdder='Fetching..',classes=format_value)
sell_at_ratio = jp.Input(a=settings_grid, placeholder='Fetching...', classes=format_value)
jp.Div(a=settings_grid, text="Buy at Ratio", classes=format_lable)
jp.Div(a=settings_grid, text="Sell at Ratio", classes=format_lable)
jp.Button(a=settings_grid, text="Update Config", click = update_config,
            drift = drift_field, gain = gain_field, ba_ratio = buy_at_ratio, sa_ratio = sell_at_ratio,
            classes='items-center bg-blue-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-blue-200 hover:text-blue-900')


# MANAGE SCRIPT

script_block = jp.Div(a=page, text="Manage Script", classes="rounded-md bg-white shadow-lg m-2 p-2 text-lg font-medium")
input_grid = jp.Div(a=script_block)
script_input_box = jp.Input(a=input_grid, placeholder="NSE Script code", classes="border-color:rgb(0 0 0)")
jp.Div(a=script_block, text="Add/Delete stock", classes=format_lable)
script_box_grid_1 = jp.Div(a=script_block, classes="grid grid-cols-2 align-items:stretch")
jp.Button(a=script_box_grid_1, text="Add Stock", click = add_stock_event,
            script_code = script_input_box,
            classes='items-center bg-blue-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-blue-200 hover:text-blue-900')

jp.Button(a=script_box_grid_1, text="Remove Stock", click = remove_stock_event,
            script_code = script_input_box,
            classes='items-center bg-blue-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-blue-200 hover:text-blue-900')

jp.Div(a=script_block, text="Manual Override", classes=format_lable)
script_box_grid_2 = jp.Div(a=script_block, classes="grid grid-cols-2 align-items:stretch")
jp.Button(a=script_box_grid_2, text="Manual Buy", click = manual_buy_event,
            script_code = script_input_box,
            classes='items-center bg-blue-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-blue-200 hover:text-blue-900')

jp.Button(a=script_box_grid_2, text="Manual Sell", click = manual_sell_event,
            script_code = script_input_box,
            classes='bg-blue-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-blue-200 hover:text-blue-900')

jp.Button(a=page, text="Emergency Stop", click = manual_stop_event,
            script_code = script_input_box,
            classes='bg-red-500 text-white m-2 py-2 py-1 w-1/2 rounded-full '
                    'hover:bg-red-200 hover:text-blue-900')

# UI ENDS HERE_________________________________________________________________

async def app_loop():
    global buy_display, total_value, invested_value, gain_value, balance_summary, drift_display_value
    while True:
        clock_div.text = "Last updated: " + time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
        run_status = sweetloop.Status()
        status_block.text = f"Status : {run_status[0]}"

        summary_data = stock_data.get_summary_data()
        total_value.text = summary_data[0]
        invested_value.text = summary_data[1]
        gain_value.text = summary_data[2]
        drift_field.placeholder = str(stock_data.drift_value()) + " %"
        gain_field.placeholder = str(stock_data.gain_value()) + " %"
        buy_at_ratio.placeholder = str(stock_data.get_ratio('buy'))
        sell_at_ratio.placeholder = str(stock_data.get_ratio('sell'))


        if run_status[1] == True:
            sweetloop.loop_operation()

        balance_summary.text = str(stock_data.get_balance())

        try:
            sell_display.delete_components()
        except:
            stock_data.raise_error_code(2)

        buy_list = stock_data.get_display('SELL_TABLE')
        for stock_detail in buy_list:
            grid_sell = jp.Div(a=sell_display, classes="grid grid-cols-2 gap-1")
            jp.Div(a=grid_sell, text=stock_detail[0], classes="font-medium text-base pt-3")
            jp.Div(a=grid_sell, text=str(stock_detail[2]), classes="text-right text-base font-medium pt-3")
            jp.Div(a=grid_sell, text=str(stock_detail[4]), classes="font-extralight text-xs")
            jp.Div(a=grid_sell, text=str(stock_detail[1]), classes="text-right font-extralight text-xs")

        try:
            buy_display.delete_components()
        except:
            stock_data.raise_error_code(3)

        buy_list = stock_data.get_display('BUY_TABLE')
        for stock_detail in buy_list:
            grid_buy = jp.Div(a=buy_display, classes="grid grid-cols-2 gap-1")
            jp.Div(a=grid_buy, text=stock_detail[0], classes="font-medium text-base pt-3")
            jp.Div(a=grid_buy, text=str(stock_detail[1]), classes="text-right text-base font-medium pt-3")
            jp.Div(a=grid_buy, text=str(stock_detail[2]), classes="font-extralight text-xs")
            jp.Div(a=grid_buy, text=str(stock_detail[3]), classes="text-right font-extralight text-xs")

        jp.run_task(wp.update())
        await asyncio.sleep(1)

async def clock_init():
    jp.run_task(app_loop())

async def clock_test():
    return wp

jp.justpy(clock_test, startup=clock_init)
