from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# 各クラスのデータベース
database = {
    "北館":{},
    "南館":{
        "1A":["1-A", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1B":["1-B", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1C":["1-C", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1D":["1-D", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1E":["1-E", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1F":["1-F", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
        "1G":["1-G", "混雑していない", ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))],
    },
    "三号館":{}
}

# メインページ 館ごとに混雑状況を確認できる
@app.route("/<tabname>")
def main(tabname):
    return render_template("index.html", tabname=tabname, data=database[tabname])

# 混雑状況の更新ページ
@app.route("/update/<tabname>", methods=["GET"])
def update(tabname):
    _class = request.args.get("class")
    congestion = request.args.get("congestion")
    print(_class, congestion)
    if _class != None and congestion != None:
        database[tabname][_class][1] = congestion
        database[tabname][_class][2] = ":".join(map(str, [datetime.datetime.now().hour, datetime.datetime.now().minute]))
        print(database)
    return render_template("update.html",tabname=tabname, data=database[tabname])

# /に来たら北館ページに遷移
@app.route("/")
def redi():
    return redirect("/北館")

# 実働時にはdebugはオフに
# 今回は実験がてら、flaskのテストサーバーではなく、wsgiのサーバーを使って実装したい
if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)