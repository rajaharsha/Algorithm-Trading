# scheduling a trade algorithm on frequency basis like once in a day or week or month
# declare the global variables in intialize funcation.
# here we are declaring AAPL stock name

def initialize(context):
    
    set_benchmark(sid(8554)) # declare benchmark (default is S&P 500)
    context.aapl = sid(24)
    context.tesla = sid(39840)
    
    schedule_function(ma_crossover_handling, # user trading logic function
                      date_rules.every_day(), # frequency of function call 
                      time_rules.market_open(hours=1) # set start time n hours after market opens
                     )
        
def ma_crossover_handling(context, data):
    
    # pull the upto date data and executes the trading logic.
    hist = data.history(context.aapl, 'price', 50,'1d')
    log.info(hist.head())
    
    # calculate average stock price from the start date of trading.
    sma_50 = hist.mean()
     
    # calculate average stock price for last 20 days of current date.
    sma_20 = hist[-20:].mean()
    
    # function to check if previous orders are still alive.
    open_orders = get_open_orders()
    
    ####################
    # Trading Strategy #
    ####################
    """
    1) Check for open orders before placing a Buy or Sell order.
    2) Average Stock Price for last 20 days trade is greater than 
       Average Stock Price from the starting day then - Buy
    3) Average Stock Price for last 20 days trade is less than 
       Average Stock Price from the starting day then - Sell
    """   
    if sma_20 > sma_50:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, 1.0)
    elif sma_50 > sma_20:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, -1.0)
            
    record(leverage = context.account.leverage)