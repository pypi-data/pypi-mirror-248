Polygon.io Backtesting
===================================

Polygon.io backtester allows for flexible and robust backtesting. It uses the polygon.io API to fetch pricing data for stocks, options, forex, and cryptocurrencies. This backtester simplifies the process of getting pricing data; simply use the PolygonDataSource and it will automatically fetch pricing data when you call `get_last_price()` or `get_historical_prices()`.

As of this writing, polygon provides up to 2 years of historical data for free. If you pay for an API you can get many years of data and the backtesting will download data much faster because it won't be rate limited.

This backtesting method caches the data on your computer making it faster for subsequent backtests. So even if it takes a bit of time the first time, the following backtests will be much faster.

To use this feature, you need to obtain an API key from polygon.io, which is free and you can get in the Dashboard after you have created an account. You must then replace `YOUR_POLYGON_API_KEY` with your own key in the code.

Start by importing the PolygonDataBacktesting as follows:

.. code-block:: python

    from backtesting import PolygonDataBacktesting

Set the start and end dates for the backtest:

.. code-block:: python

    backtesting_start = datetime.datetime(2023, 1, 1)
    backtesting_end = datetime.datetime(2023, 5, 1)


Optional: Set the quote asset (usually only required for crypto, default is USD) and the trading fee.

.. code-block:: python

    quote_asset = Asset(symbol="USDT", asset_type="crypto")
    trading_fee = TradingFee(percent_fee=0.001)

Finally, run the backtest:

.. code-block:: python

    trader = Trader(backtest=True)
    data_source = PolygonDataBacktesting(
        datetime_start=backtesting_start,
        datetime_end=backtesting_end,
        api_key="YOUR_POLYGON_API_KEY",
        has_paid_subscription=False, # Set this to True if you have a paid subscription to polygon.io (False assumes you are using the free tier)
    )
    broker = BacktestingBroker(data_source)
    crypto_strat = CryptoEMACross(
        broker=broker,
        backtesting_start=backtesting_start,
        backtesting_end=backtesting_end,
        quote_asset=quote_asset,
        benchmark_asset=Asset(symbol="BTC", asset_type="crypto")
        buy_trading_fees=[trading_fee],
        sell_trading_fees=[trading_fee],
    )
    trader.add_strategy(crypto_strat)
    trader.run_all()

Here's another example but for for stocks:

.. code-block:: python

    from datetime import datetime
    from lumibot.backtesting import PolygonDataBacktesting
    from lumibot.strategies import Strategy

    class MyStrategy(Strategy):
        parameters = {
            "symbol": "AAPL",
        }

        def initialize(self):
            self.sleeptime = "1D"

        def on_trading_iteration(self):
            if self.first_iteration:
                symbol = self.parameters["symbol"]
                price = self.get_last_price(symbol)
                qty = self.portfolio_value / price
                order = self.create_order(symbol, quantity=qty, side="buy")
                self.submit_order(order)

    if __name__ == "__main__":
        backtesting_start = datetime(2023, 1, 1)
        backtesting_end = datetime(2023, 5, 1)

        trader = Trader(backtest=True)
        data_source = PolygonDataBacktesting(
            datetime_start=backtesting_start,
            datetime_end=backtesting_end,
            api_key="YOUR_POLYGON_API_KEY",
            has_paid_subscription=False, # Set this to True if you have a paid subscription to polygon.io (False assumes you are using the free tier)
        )
        broker = BacktestingBroker(data_source)
        my_strat = MyStrategy(
            broker=broker,
            backtesting_start=backtesting_start,
            backtesting_end=backtesting_end,
            benchmark_asset=Asset(symbol="BTC", asset_type="crypto")
        )
        trader.add_strategy(crypto_strat)
        trader.run_all()

In summary, the polygon.io backtester is a powerful tool for fetching pricing data for backtesting various strategies. With its capability to cache data for faster subsequent backtesting and its easy integration with polygon.io API, it is a versatile choice for any backtesting needs.
