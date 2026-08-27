from flask import Flask, render_template, request
import pandas as pd
from logic import diagnose
from colors import (color_rsi,color_ma25,color_vol)

app = Flask(__name__)

# @app.route ルート定義
# フォームの初期表示
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", table_html=None)

# @app.route ルート定義
@app.route("/upload", methods=["POST"])
# データ処理＆表示
def upload():    
    file = request.files["csv_file"]
    df = pd.read_csv(file)
    
    # ロジックを実行
    df = diagnose(df)

    # 最新60件だけにする
    df = df.sort_values("日付", ascending=False).head(60).reset_index(drop=True)

    # 必要な項目だけ選ぶ
    df_selected = df[[
        "日付",
        "終値",
        "level",
        "MA25_dis_type",
        "vol_type",
        "RSI14_type",
    ]].rename(columns={
        "level": "MACD判定",
        "MA25_dis_type": "25日乖離判定",
        "vol_type": "出来高判定",
        "RSI14_type": "RSI判定",
    })

    # 色付け（Styler）
    def color_row(row):
        return [f'background-color: #{df.loc[row.name, "level_color"]}'] * len(row)


    # # HTMLに変換
    # apply 行全体 , map セル単位
    styler = (
        df_selected
            .style
            .format({
                "終値": "{:.2f}",
            })
            .apply(color_row, axis=1)  # 行色（MACD level）
            .map(color_rsi, subset=["RSI判定"])  # RSIセル
            .map(color_ma25, subset=["25日乖離判定"])  # MA25乖離セル
            .map(color_vol, subset=["出来高判定"])  # volセル
            .set_properties(**{"text-align": "center"})
    )

    table_html = styler.to_html()

    return render_template("index.html", table_html=table_html)

@app.route("/clear")
def clear():
    return render_template("index.html", table_html=None)

# 実行（ローカル用）
if __name__ == "__main__":
    app.run(debug=True)

