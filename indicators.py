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

