import pandas as pd

def output(df):
    lines = []

    # 直近5日分を取り出す（足りないときはあるだけ）
    n = min(5, len(df))
    target = df.iloc[-n:]   # 例：[-5:] → 5日分

    for _, row in target[::-1].iterrows():  # 新しい順に並べる
        line = (
            f"日付：{row['Date'].strftime('%m/%d')}\n"
            f"終値：{row['Close']:.0f}円　"
            f"MACD_level：{row['level']}　"
            f"出来高：{row['Volume']:.0f}（{row['vol_type']}）　"
            f"RSI：{row['RSI14']:.0f}（{row['RSI14_type']}）　"
            f"ローソク足１：{row['candle1']}　"
            f"ローソク足２：{row['candle2']}　"
            f"ローソク足３：{row['candle3']}"
        )
        lines.append(line)

    # 改行で結合
    return "\n".join(lines)