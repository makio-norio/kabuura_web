import pandas as pd
from indicators import (calc_rsi,candlestick_type1,candlestick_type2,candlestick_type3,)

def diagnose(df):
    
    # print("=== df.columns ===")
    # print(df.columns)
    # print("=== df.head() ===")
    # print(df.head())
    # print("=== df.dtypes ===")
    # print(df.dtypes)
    # print("hello!")
    # print("df:", df)
    # # ma25乖離率
    df["MA25"] = df["Close"].rolling(25).mean()
    df["MA25_dis"] = (df["Close"] - df["MA25"]) / df["MA25"] * 100
    df["MA25_dis_type"] = None
            
    df.loc[df["MA25_dis"] < -12, "MA25_dis_type"] = "低迷ゾーン"
    df.loc[(df["MA25_dis"] >= -12) & (df["MA25_dis"] < -7), "MA25_dis_type"] = "かなり下"
    df.loc[(df["MA25_dis"] >= -7) & (df["MA25_dis"] < -3), "MA25_dis_type"] = "やや下"
    df.loc[(df["MA25_dis"] >= -3) & (df["MA25_dis"] < 0), "MA25_dis_type"] = "ちょい下"
    df.loc[(df["MA25_dis"] >= 0) & (df["MA25_dis"] < 3), "MA25_dis_type"] = "ちょい上"
    df.loc[(df["MA25_dis"] >= 3) & (df["MA25_dis"] < 7), "MA25_dis_type"] = "やや上"
    df.loc[(df["MA25_dis"] >= 7) & (df["MA25_dis"] < 12), "MA25_dis_type"] = "かなり上"
    df.loc[df["MA25_dis"] >= 12, "MA25_dis_type"] = "過熱ゾーン"
     
    # macd
    df["EMA12"] = df["Close"].ewm(span=12).mean()
    df["EMA26"] = df["Close"].ewm(span=26).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9).mean()
    # macd level  series(全行)
    df["level"] = None
    df.loc[(df["MACD"] > 0) & (df["Signal"] <= 0), "level"] = 3
    df.loc[(df["MACD"] > 0) & (df["Signal"] > 0) & (df["MACD"] > df["Signal"]), "level"] = 5
    df.loc[(df["MACD"] > 0) & (df["Signal"] > 0) & (df["MACD"] <= df["Signal"]), "level"] = 4
    df.loc[(df["MACD"] <= 0) & (df["MACD"] > df["Signal"]), "level"] = 2
    df.loc[(df["MACD"] <= 0) & (df["MACD"] <= df["Signal"]), "level"] = 1
    # 色コード
    level_colors = {
        1: "FFFF00",
        2: "FDE9D9",
        3: "FABF8F",
        4: "B8CCE4",
        5: "FF9191",
    }
    df["level_color"] = df["level"].map(level_colors)

    df["RSI14"] = calc_rsi(df["Close"], 14)
    df["RSI14_type"] = None 
    df.loc[(df["RSI14"] >= 70) , "RSI14_type"] = "かなり買われ"
    df.loc[(df["RSI14"] >= 55) & (df["RSI14"] < 70), "RSI14_type"] = "やや買われ"
    df.loc[(df["RSI14"] >= 45) & (df["RSI14"] < 55), "RSI14_type"] = "中立"
    df.loc[(df["RSI14"] >= 30) & (df["RSI14"] < 45), "RSI14_type"] = "やや売られ"
    df.loc[(df["RSI14"] >= 0) & (df["RSI14"] < 30) , "RSI14_type"] = "かなり売られ"

    df["vol_ma5"] = df["Volume"].rolling(5).mean()
    df["vol_dis"] = (df["Volume"] - df["vol_ma5"]) / df["vol_ma5"] * 100
    df["vol_type"] = None
    df.loc[df["vol_dis"] >= 50, "vol_type"] = "かなり増"
    df.loc[(df["vol_dis"] >= 20) & (df["vol_dis"] < 50), "vol_type"] = "増えてる"
    df.loc[(df["vol_dis"] > -20) & (df["vol_dis"] < 20), "vol_type"] = "変化なし"
    df.loc[(df["vol_dis"] <= -20) & (df["vol_dis"] > -50), "vol_type"] = "減ってる"
    df.loc[df["vol_dis"] <= -50, "vol_type"] = "かなり減"

    # ローソク足
    df["candle1"] = df.apply(
        lambda r: candlestick_type1(
            r["Open"],
            r["Close"],
            r["High"],
            r["Low"],   
        ),
        axis=1
    )
    df["candle2"] = df.apply(
        lambda r: candlestick_type2(
            df.loc[r.name - 1, "Open"],    # 前日
            df.loc[r.name - 1, "Close"],
            df.loc[r.name - 1, "High"],
            df.loc[r.name - 1, "Low"],
            r["Open"],                     # 当日
            r["Close"],
            r["High"],
            r["Low"],   
        ) if r.name >= 1 else "",
        axis=1
    )
    
    df["candle3"] = df.apply(
        lambda r: candlestick_type3(
            df.loc[r.name - 2, "Open"],    # 2日前
            df.loc[r.name - 2, "Close"],
            df.loc[r.name - 2, "High"],
            df.loc[r.name - 2, "Low"],
            df.loc[r.name - 1, "Open"],    # 前日
            df.loc[r.name - 1, "Close"],
            df.loc[r.name - 1, "High"],
            df.loc[r.name - 1, "Low"],
            r["Open"],                     # 当日
            r["Close"],
            r["High"],
            r["Low"],   
        ) if r.name >= 2 else "",
        axis=1
    )

    return df
