from flask import Flask, render_template, request, session
from ice_cream import get_flavors
import random
import json
import requests

app = Flask(__name__)
app.secret_key = "icecream2024"
app.jinja_env.globals.update(enumerate=enumerate)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # 获取天气
    use_api = request.form.get("use_api")
    if use_api == "y":
        city = request.form.get("city")
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            temperature = float(data["current_condition"][0]["temp_C"])
            humidity = float(data["current_condition"][0]["humidity"])
        except:
            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
    else:
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])

    dislike = request.form.get("dislike", "")

    # 获取口味列表
    mood, flavors = get_flavors(temperature, humidity)

    if dislike in flavors:
        flavors.remove(dislike)

    # 读取收藏
    favorites = session.get("favorites", [])

    # 加权推荐
    if flavors:
        pool = list(flavors)
        weights = [2 if f in favorites else 1 for f in pool]
        for f in favorites:
            if f not in pool:
                pool.append(f)
                weights.append(0.5)
        result = random.choices(pool, weights=weights, k=1)[0]
    else:
        result = None

    # 保存历史
    history = session.get("history", [])
    if result:
        history.append(result)
    session["history"] = history

    return render_template("index.html",
        mood=mood,
        result=result,
        temperature=temperature,
        humidity=humidity,
        favorites=favorites,
        history=history
    )

@app.route("/favorite", methods=["POST"])
def favorite():
    item = request.form.get("item")
    favorites = session.get("favorites", [])
    if item and item not in favorites:
        favorites.append(item)
        session["favorites"] = favorites
    return render_template("index.html",
        favorites=favorites,
        history=session.get("history", []),
        message=f"❤️ 已收藏「{item}」！"
    )

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return render_template("index.html", message="🗑️ 历史记录和收藏已清空！")

if __name__ == "__main__":
    app.run(debug=True)