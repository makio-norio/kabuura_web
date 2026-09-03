import pandas as pd
import numpy as np
from indicators import (calc_rsi,candlestick_type1,candlestick_type2,candlestick_type3)

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

    # ma5
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA5_slope_pct_3d"] = df["MA5"].pct_change(3) * 100 / 3 
    df["MA5_slope_std"] = df["MA5_slope_pct_3d"].rolling(10, min_periods=10).std()
    score = df["MA5_slope_pct_3d"] / df["MA5_slope_std"]
    conditions = [
        (score < -2.0),
        (score < -0.5),
        (score < 0.5) ,
        (score < 2.0),
    ]
    choices = [ "強い下降","ゆるやか下降","よこよこ","ゆるやか上昇"]
    df["MA5_score_type"] = np.select(
        conditions,
        choices,
        default="強い上昇",
    )
    
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

    df["RSI"] = calc_rsi(df["Close"], 5)
    df["RSI_type"] = None 
    df.loc[(df["RSI"] >= 70) , "RSI_type"] = "かなり買われ"
    df.loc[(df["RSI"] >= 55) & (df["RSI"] < 70), "RSI_type"] = "やや買われ"
    df.loc[(df["RSI"] >= 45) & (df["RSI"] < 55), "RSI_type"] = "中立"
    df.loc[(df["RSI"] >= 30) & (df["RSI"] < 45), "RSI_type"] = "やや売られ"
    df.loc[(df["RSI"] >= 0) & (df["RSI"] < 30) , "RSI_type"] = "かなり売られ"

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

    df.loc[
        (df["level"] == 3) &
        (df["MA25_dis_type"].isin(["ちょい上", "やや上", "かなり上"])) &
        (df["vol_type"].isin(["増えてる", "かなり増"])) &
        (df["RSI_type"].isin(["中立", "やや買われ"])),
        "composite_type"
    ] = "上昇のはじまりかも"
    df.loc[
        (df["MA25_dis_type"].isin(["ちょい下", "やや下"])) &
        (df["level"].isin([4, 5])) &
        (df["RSI_type"].isin(["やや売られ", "かなり売られ"])) &
        (df["vol_type"].isin(["減ってる", "かなり減"])),
        "composite_type"
    ] = "押し目かもしれませんがそのまま下がることも。。。"
    df.loc[
        (df["MA25_dis_type"].isin(["かなり上", "過熱ゾーン"])) &
        (df["level"] == 5) &
        (df["RSI_type"] == "かなり買われ") &
        (df["vol_type"] == "かなり増"),
        "composite_type"
    ] = "天井圏かもしれません。過熱に注意しましょう"
    df.loc[
        (df["MA25_dis_type"].isin(["ちょい上", "やや上"])) &
        (df["level"].isin([4, 3, 2])) &
        (df["vol_type"].isin(["減ってる", "変化なし"])),
        "composite_type"
    ] = "上昇の終わりでしょう"
    df.loc[
        (df["MA25_dis_type"].isin(["やや下", "かなり下"])) &
        (df["level"].isin([3, 4])) &
        (df["RSI_type"].isin(["やや買われ", "かなり買われ"])) &
        (df["vol_type"] == "かなり増"),
        "composite_type"
    ] = "だまし上げの可能性があり。注意しましょう"
    df.loc[
        (df["MA25_dis_type"] == "低迷ゾーン") &
        (df["level"] == 1) &
        (df["RSI_type"] == "かなり売られ") &
        (df["vol_type"].isin(["かなり減", "減ってる"])),
        "composite_type"
    ] = "大底からの一筋の光がみえます"
    df["composite_type"] = df["composite_type"].fillna("ぼちぼちです。")

    return df
