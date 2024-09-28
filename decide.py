from tradingview_ta import TA_Handler
import yfinance as yf

class Decide:

    def buy(nse_code,drift_target,buy_ratio):
        #drift target is the value value at which
        buy_flags = 1
        #Get 5D previous high Data
        history_data = yf.Ticker(str(nse_code)+'.NS').history(period = '5d').to_dict()
        prev_week_high = list(history_data.get('High').values())[0]

        #Get Live Trading Price
        ltp = yf.Ticker(str(nse_code) + '.NS').info.get('currentPrice')

        drift_percent = (prev_week_high-ltp)/prev_week_high * 100

        if drift_percent >= drift_target:
            buy_flags = buy_flags + 1


        handler = TA_Handler(
            screener="india",
            exchange="NSE",
            symbol=nse_code,
            interval="5m"
        )
        buy_score = handler.get_analysis().summary.get('BUY')
        sell_score = handler.get_analysis().summary.get('SELL')

        buy_strength = buy_score - sell_score

        if buy_strength >= buy_ratio:
            buy_flags = buy_flags + 1

        if buy_flags == 3:
            return [True, buy_flags, ltp, buy_ratio]
        else:
            return [False,buy_flags, ltp, buy_ratio]

    def sell(nse_code, purchase_price,gain_target,sell_ratio):

        # Get Live Trading Price
        ltp = yf.Ticker(str(nse_code) + '.NS').info.get('currentPrice')

        gain_percentage = (ltp-purchase_price)/purchase_price * 100

        handler = TA_Handler(
            screener="india",
            exchange="NSE",
            interval="5m",
            symbol=nse_code
        )

        buy_score = handler.get_analysis().summary.get('BUY')
        sell_score = handler.get_analysis().summary.get('SELL')

        buy_strength = buy_score - sell_score

        if gain_percentage > gain_target or buy_strength < sell_ratio or gain_percentage < -7:
            return [True, 2, ltp]

        else:
            return [False, 1, ltp]





