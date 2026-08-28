from flask import Flask, render_template, request
import re
import pandas as pd
import yfinance as yf
from logic import diagnose
from put_out import output
from colors import (color_rsi,color_ma25,color_vol)

app = Flask(__name__)

# @app.route ルート定義
# フォームの初期表示
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None, error=None)

# @app.route ルート定義
@app.route("/upload", methods=["POST"])
# データ処理＆表示
def upload(): 
    result = None
    error = None
    code = request.form.get("code", "").strip()

    # 半角英数字4文字のみ
    if not re.fullmatch(r"[0-9A-Za-z]{4}", code):
        error = "銘柄コードは半角英数字4文字で入力してください"
        return render_template("index.html", result=None, error=error)
    
    # 日本株のティッカー（例：7203.T）
    ticker = f"{code}.T"

    try:
        df = yf.download(ticker, period='6mo', interval='1d', auto_adjust=False)        
        
        if df.empty:
            error = "データが取得できませんでした（コードが間違っている可能性があります）"
            return render_template("index.html", result=None, error=error)
        
        # MultiIndex をフラット化
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # index=dateをresetして項目化する
        df = df.reset_index()

        # 編集
        df = diagnose(df)

        # 出力用表示
        result = output(df)
        
        return render_template("index.html", result=result, error=None)
    except Exception :
        return render_template("index.html", result=result, error= "データ取得中にエラーが発生しました")
    
@app.route("/clear")
def clear():
    return render_template("index.html", result=None, error=None)

# 実行（ローカル用）
if __name__ == "__main__":
    app.run(debug=True)

