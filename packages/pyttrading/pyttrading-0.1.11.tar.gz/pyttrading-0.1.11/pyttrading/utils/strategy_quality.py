
def strategy_quality(config, data):

    metrics = data.metrics
    save_mode = False
    trades = metrics.get('Trades')
    profit_factor = metrics.get('ProfitFactor')

    if trades >= config.min_trades and profit_factor >= config.min_profit_factor:
        if metrics.get('best_return_sl') > metrics.get('best_return'):
            save_mode = True

    return save_mode