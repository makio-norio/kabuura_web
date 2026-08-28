import pandas as pd

def calc_rsi(close_series, period):
    delta = close_series.diff()                  # ← ここで前日比を計算！
    gain = delta.where(delta > 0, 0)             # 上昇分だけ抽出
    loss = -delta.where(delta < 0, 0)            # 下落分だけ抽出（符号を正にする）
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss                     # 𝑅𝑆 = 14日間の平均上昇幅 / 14日間の平均下落幅
    rsi = 100 - (100 / (1 + rs))                 # 𝑅𝑆𝐼 = 100 − (100 / 1 + 𝑅𝑆)
    return rsi

def candlestick_type1(open, close, high, low):
    body = abs(close - open)
    upper = high - max(open, close)
    lower = min(open, close) - low
    total = high - low
    
    # 陽線・陰線・同値
    if close > open:
        base = "🌞陽線"
    elif close < open:
        base = "🌙陰線"
    else:
        base = "同値"
    # 大陽線・大陰線
    if body > total * 0.7:
        if close > open:
            return "🌞🌞大陽線"
        else:
            return "🌙🌙大陰線"
    # コマ足（実体が小さい）
    if body < total * 0.2:
        return "😑コマ足"
    # カラカサ（下ヒゲ長い）
    if lower > body * 2 and upper < body * 0.3:
        return "🦾😤カラカサ"
    # トンカチ（上ヒゲ長い）
    if upper > body * 2 and lower < body * 0.3:
        return "😭トンカチ"
    return base

def candlestick_type2(prev1_open, prev1_close, prev1_high, prev1_low,
                            open, close, high, low):

    # 包み足（エンゴルフィング）
    if high > prev1_high and low < prev1_low:
        if close > open:
            return "😤陽の包み足"
        else:
            return "😱陰の包み足"

    # はらみ足（インサイドバー）
    if high < prev1_high and low > prev1_low:
        return "🤔はらみ足"

    # ===== 二兵（強弱つき） =====
    prev1_body = abs(prev1_close - prev1_open)
    today_body = abs(close - open)

    # 陽の二兵
    if prev1_close > prev1_open and close > open:
        strength = "弱"
        if today_body > prev1_body:
            strength = "強"
        if close > prev1_high:
            strength = "超強"
        return f"🙂陽の二兵({strength})"

    # 陰の二兵
    if prev1_close < prev1_open and close < open:
        strength = "弱"
        if today_body > prev1_body:
            strength = "強"
        if close < prev1_low:
            strength = "超強"
        return f"😨陰の二兵({strength})"

    return "なし"

def candlestick_type3(prev2_open,prev2_close,prev2_high,prev2_low,prev1_open,prev1_close,prev1_high,prev1_low,open,close,high,low):
    # c1 → 3日前, c2 → 2日前, c3 → 当日
    # 三兵
    if prev2_close > prev2_open and prev1_close > prev1_open and close > open :
        if prev2_low < prev1_low < low and prev2_high < prev1_high < high:
            return "🤩三兵"
    # 三羽烏
    if prev2_close < prev2_open and prev1_close < prev1_open and close < open :
        if prev2_high > prev1_high > high and prev2_low > prev1_low > low :
            return "🤢三羽烏"
    return "なし"
