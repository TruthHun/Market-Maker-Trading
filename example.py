# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *
'''
本策略通过不断对CZCE.CF801进行:
买(卖)一价现价单开多(空)仓和卖(买)一价平多(空)仓来做市
并以此赚取差价
回测数据为:CZCE.CF801的tick数据
回测时间为:2017-09-29 11:25:00到2017-09-29 11:30:00
需要特别注意的是:本平台对于回测对限价单固定完全成交,本例子 仅供参考.
敬请通过适当调整回测参数
1.backtest_commission_ratio回测佣金比例
2.backtest_slippage_ratio回测滑点比例
3.backtest_transaction_ratio回测成交比例
以及优化策略逻辑来达到更贴近实际的回测效果
'''
def init(context):
    # 订阅CZCE.CF801的tick数据
    context.symbol = 'CZCE.CF801'
    subscribe(symbols=context.symbol, frequency='tick')
def on_tick(context, tick):
    quotes = tick['quotes'][0]
    # 获取持有的多仓
    positio_long = context.account().position(symbol=context.symbol, side=PositionSide_Long)
    # 获取持有的空仓
    position_short = context.account().position(symbol=context.symbol, side=PositionSide_Short)
    print(quotes['bid_p'])
    print(quotes['ask_p'])
    # 没有仓位则双向开限价单
    # 若有仓位则限价单平仓
    if not positio_long:
        # 获取买一价
        price = quotes['bid_p']
        print('买一价为: ', price)
        order_target_volume(symbol=context.symbol, volume=1, price=price, order_type=OrderType_Limit,
                            position_side=PositionSide_Long)
        print('CZCE.CF801开限价单多仓1手')
    else:
        # 获取卖一价
        price = quotes['ask_p']
        print('卖一价为: ', price)
        order_target_volume(symbol=context.symbol, volume=0, price=price, order_type=OrderType_Limit,
                            position_side=PositionSide_Long)
        print('CZCE.CF801平限价单多仓1手')
    if not position_short:
        # 获取卖一价
        price = quotes['ask_p']
        print('卖一价为: ', price)
        order_target_volume(symbol=context.symbol, volume=1, price=price, order_type=OrderType_Limit,
                            position_side=PositionSide_Short)
        print('CZCE.CF801卖一价开限价单空仓')
    else:
        # 获取买一价
        price = quotes['bid_p']
        print('买一价为: ', price)
        order_target_volume(symbol=context.symbol, volume=0, price=price, order_type=OrderType_Limit,
                            position_side=PositionSide_Short)
        print('CZCE.CF801买一价平限价单空仓')
if __name__ == '__main__':
    '''
    strategy_id策略ID,由系统生成
    filename文件名,请与本文件名保持一致
    mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
    token绑定计算机的ID,可在系统设置-密钥管理中生成
    backtest_start_time回测开始时间
    backtest_end_time回测结束时间
    backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
    backtest_initial_cash回测初始资金
    backtest_commission_ratio回测佣金比例
    backtest_slippage_ratio回测滑点比例
    backtest_transaction_ratio回测成交比例
    '''
    run(strategy_id='strategy_id',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='token_id',
        backtest_start_time='2017-09-29 11:25:00',
        backtest_end_time='2017-09-29 11:30:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=500000,
        backtest_commission_ratio=0.00006,
        backtest_slippage_ratio=0.0001,
        backtest_transaction_ratio=0.5)