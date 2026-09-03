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

def composite_fortune(ma25, macd_level, rsi_type, vol_type):
    # 上昇初動
    if macd_level == 3 and ma25 in ["ちょい上", "やや上", "かなり上"] \
       and vol_type in ["増えてる", "かなり増"] \
       and rsi_type in ["中立", "やや買われ"]:
        return "上昇初動（本命）"

    # 押し目
    if ma25 in ["ちょい下", "やや下"] \
       and macd_level in [4, 5] \
       and rsi_type in ["やや売られ", "かなり売られ"] \
       and vol_type in ["減ってる", "かなり減"]:
        return "押し目（買い場候補）"

    # 過熱注意
    if ma25 in ["かなり上", "過熱ゾーン"] \
       and macd_level == 5 \
       and rsi_type == "かなり買われ" \
       and vol_type == "かなり増":
        return "過熱注意（天井圏）"

    # 失速
    if ma25 in ["ちょい上", "やや上"] \
       and macd_level in [4, 3, 2] \
       and vol_type in ["減ってる", "変化なし"]:
        return "失速（上昇の終わり）"

    # 逆行高
    if ma25 in ["やや下", "かなり下"] \
       and macd_level in [3, 4] \
       and rsi_type in ["やや買われ", "かなり買われ"] \
       and vol_type in ["かなり増"]:
        return "逆行高（危険）"

    # 大底候補
    if ma25 == "低迷ゾーン" \
       and macd_level == 1 \
       and rsi_type == "かなり売られ" \
       and vol_type in ["かなり減", "減ってる"]:
        return "大底候補（反発前）"

    return "中立（様子見）"

def fortune_text(type_name):
    if type_name == "上昇初動（本命）":
        return "上昇初動です。位置も良く、出来高の裏付けもあり、勢いが出始めています。短期的には上方向を試しやすい展開です。"

    if type_name == "押し目（買い場候補）":
        return "上昇トレンド中の押し目です。RSIが冷えて出来高も枯れており、反発しやすい位置です。"

    if type_name == "過熱注意（天井圏）":
        return "過熱ゾーンです。勢いは強いものの、買われすぎと出来高急増が重なり、天井圏の可能性があります。"

    if type_name == "失速（上昇の終わり）":
        return "上昇が失速しています。出来高が減り、勢いが弱まっています。短期的には注意が必要です。"

    if type_name == "逆行高（危険）":
        return "位置が悪い中で出来高だけ増えて上昇しています。だまし上げの可能性があり注意が必要です。"

    if type_name == "大底候補（反発前）":
        return "低迷ゾーンで売りが枯れています。反発の可能性がありますが、トレンドは弱いため慎重に。"

    return "特筆すべきシグナルはなく、中立です。"
