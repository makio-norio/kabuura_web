import pandas as pd

def output(df):
    result = None
    last = df.iloc[-1]
    prev1  = df.iloc[-2]
    prev2  = df.iloc[-3]
    
    result = (
        f"日付：{last['Date'].strftime('%m/%d')}（まだ確定じゃないかも）\n"
        f"終値：{last['Close']:.0f}円　MACD_level：{last['level']}　出来高：{last['Volume']:.0f}（{last['vol_type']}）　RSI：{last['RSI14']:.0f}（{last['RSI14_type']}）\n"
        f"日付：{prev1['Date'].strftime('%m/%d')}\n"
        f"終値：{prev1['Close']:.0f}円　MACD_level：{prev1['level']}　出来高：{prev1['Volume']:.0f}（{prev1['vol_type']}）　RSI：{prev1['RSI14']:.0f}（{prev1['RSI14_type']}）"
    )

    return result