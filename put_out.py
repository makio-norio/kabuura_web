import pandas as pd

def output(df):
    lines = []

    if df.iloc[-1]["composite_type"] in [ "凶","末吉","小吉","中吉","大吉"]:
        line = (
            f"今日（{df.iloc[-1]['Date'].strftime('%m/%d')}"
            f"）の運勢：{df.iloc[-1]["composite_type"]}　～{df.iloc[-1]["MA5_score_type"]}でしょう～\n"
        )
    else :
        line = (
            f"今日（{df.iloc[-1]['Date'].strftime('%m/%d')}）の運勢：{df.iloc[-1]["composite_type"]}\n"
        )        


    lines.append(line)

    # 直近5日分を取り出す（足りないときはあるだけ）
    n = min(5, len(df))
    target = df.iloc[-n:]   # 例：[-5:] → 5日分
    for _, row in target[::-1].iterrows():  # 新しい順に並べる
        line = (
            f"日付：{row['Date'].strftime('%m/%d')}\n"
            f"終値：{row['Close']:.0f}円({row["MA25_dis_type"]})　"
            f"MACD_level：{row['level']}　"
            f"出来高：{row['Volume']:.0f}（{row['vol_type']}）　"
            f"RSI：{row['RSI']:.0f}（{row['RSI_type']}）　\n"
            f"ローソク足１：{row['candle1']}　"
            f"ローソク足２：{row['candle2']}　"
            f"ローソク足３：{row['candle3']}"
        )
        lines.append(line)

    # 改行で結合
    return "\n".join(lines)