

def color_rsi(val):
    if val in ["かなり買われ","やや買われ"]:
        return "color: #C00000"
    elif val == "中立":
        return "color: black"
    elif val in ["やや売られ","かなり売られ"]:
        return "color: blue"
    return ""

def color_ma25(val):
    if val  in [ "過熱ゾーン","かなり上","やや上","ちょい上"]:
        return "color: #C00000"
    elif val in [ "低迷ゾーン","かなり下","やや下","ちょい下"]:
        return "color: blue"
    return ""

def color_vol(val):
    if val in ["かなり増","増えてる"]:
        return "color: #C00000"
    elif val == "変化なし":
        return "color: black"
    elif val in ["減ってる","かなり減"]:
        return "color: blue"
    return ""
