# QUANT SCIENCE UNIVERSITY
# Goal: Get you started making progress with backtesting
# ****

# ENVIRONMENT INSTRUCTIONS WITH CONDA:
#   conda create -n zipline_backtesting
#   conda activate zipline_backtesting
#   conda install python
#   pip install zipline-reloaded numpy==1.26.4 plotly nbformat

# IMPORTS
from zipline.api import order_target, record, symbol
from zipline import run_algorithm
from zipline.data import bundles

import pandas as pd
import plotly.express as px
import os


# STEP 1: INGEST A DATA BUNDLE
#  * ONLY NEED TO RUN THIS ONCE.
#  * THIS BUILDS THE QUANDL FREE DATA UP TO 2018. 
#  * Instructions: https://docs.data.nasdaq.com/v1.0/docs/getting-started

os.environ["QUANDL_API_KEY"] = "YOUR_API_KEY"
bundle = "quandl"
bundles.ingest(bundle)

# STEP 2: CREATE A TRADING STRATEGY

def initialize(context):
    # Define the stock to trade
    context.asset = symbol('AAPL')
    
    # Set the historical windows
    context.short_window = 10
    context.long_window = 30

def handle_data(context, data):
    # Get historical data
    short_mavg = data.history(context.asset, 'price', context.short_window, '1d').mean()
    long_mavg = data.history(context.asset, 'price', context.long_window, '1d').mean()

    # Trading logic
    if short_mavg > long_mavg:
        # Buy signal
        order_target(context.asset, 100)
    else:
        # Sell signal
        order_target(context.asset, 0)
    
    # Record the moving averages for later analysis
    record(
        short_mavg=short_mavg, 
        long_mavg=long_mavg, 
        price=data.current(context.asset, 'price')
    )
    
# STEP 3: MAKE THE BASIC BACKTEST

# Define the backtest parameters
start = pd.Timestamp('2016-01-01')
end = pd.Timestamp('2017-12-31')
capital_base = 10000

# Run the algorithm
result = run_algorithm(
    start=start, 
    end=end, 
    initialize=initialize,
    handle_data=handle_data, 
    capital_base=capital_base,
    bundle='quandl'
)

result

# STEP 4: PLOT THE PERFORMANCE

# Plot the performance
px.line(
    result.portfolio_value, 
    title = 'Portfolio Value Over Time',
    template='simple_white'
)

# Conclusions ----
# You can do this!
# There's a lot more to learn:
# - How to backtest more complex trading strategies
# - How to measure performance
# - How to include benchmarks
# - How to use with portfolio-based strategies including rebalancing
# - And more!