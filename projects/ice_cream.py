import random
import requests

all_flavors = {
    "🍓 清爽果味": ["草莓", "芒果", "百香果", "柠檬", "荔枝", "西瓜", "黄桃", "青柠", "蓝莓", "柚子"],
    "🍫 浓郁奶味": ["香草", "牛奶", "巧克力", "榛果", "焦糖", "盐焦糖", "提拉米苏", "奥利奥"],
    "🍵 东亚特色": ["抹茶", "红豆", "芋泥", "黑芝麻", "黑糖麻薯", "桂花", "豆乳"],
    "🌿 暖心口味": ["肉桂", "黑糖", "焦糖", "薰衣草", "玫瑰"]
}

history = []
favorites = []

print("=" * 30)
print("🍦 冰淇淋推荐小程序 🍦")
print("=" * 30)

try:
    name = input("请输入你的名字：")
    print(f"\n你好，{name}！欢迎来到冰淇淋推荐中心🍦\n")

    use_api = input("要自动获取当前天气吗？(y/n)：")
    if use_api.lower() == "y":
        city = input("输入你的城市（英文，如 Beijing）：")
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            temperature = float(data["current_condition"][0]["temp_C"])
            humidity = float(data["current_condition"][0]["humidity"])
            print(f"🌤️ 已获取天气：{temperature}°C，湿度 {humidity}%\n")
        except:
            print("⚠️ 获取天气失败，请手动输入")
            temperature = float(input("请输入今天的温度（摄氏度）："))
            humidity = float(input("请输入今天的湿度（%）："))

    if humidity < 0 or humidity > 100:
        print("❌ 湿度必须在0~100之间")
        exit()

    see_all = input("要先看看所有口味吗？(y/n)：")
    if see_all.lower() == "y":
        print("\n🍦 口味大全：")
        for category, items in all_flavors.items():
            print(f"\n{category}")
            print("  ", "、".join(items))
        print()

    print("\n正在分析天气情况...\n")

    if temperature > 35:
        print("🥵 极热！清爽冰沙拯救你！")
        flavors = ["柠檬冰沙", "薄荷青柠", "椰子雪葩"]

    elif temperature > 30:
        if humidity < 50:
            print("🔥 干热天气，经典奶香最舒适！")
            flavors = ["牛奶", "香草🍦", "草莓🍓", "盐焦糖"]
        else:
            print("😮‍💨 闷热潮湿，来点清爽果味解腻！")
            flavors = ["荔枝玫瑰", "百香果", "西瓜雪葩"]

    elif temperature >= 25:
        if humidity < 60:
            print("😊 温暖舒适，果味奶味都很配！")
            flavors = ["草莓🍓", "抹茶", "蓝莓"]
        else:
            print("🌫️ 有点闷，酸甜果味提提神！")
            flavors = ["柚子", "黄桃", "芒果"]

    elif temperature >= 15:
        print("🙂 温和天气，来点浓郁的！")
        flavors = ["巧克力🍫", "榛果", "提拉米苏", "红豆"]

    elif temperature >= 5:
        print("🌥️ 有点凉，选暖心口味吧！")
        flavors = ["黑糖麻薯", "芋泥", "焦糖", "肉桂"]

    else:
        print("🥶 这么冷还吃冰？！钻被窝去！")
        flavors = []

    dislike = input("有不喜欢的口味吗？输入口味名排除，没有就直接回车：")
    if dislike in flavors:
        flavors.remove(dislike)
        print(f"✅ 已排除「{dislike}」")
    elif dislike != "":
        print("⚠️ 口味列表里没有这个，跳过～")

    while flavors:
        # 构建候选列表和权重
        pool = list(flavors)
        weights = [2 if f in favorites else 1 for f in pool]

        # 收藏但不在当前列表的口味，加1%概率
        for f in favorites:
            if f not in pool:
                pool.append(f)
                weights.append(0.5)

        recommendation = random.choices(pool, weights=weights, k=1)[0]

        print(f"{name}，推荐：", recommendation)
        history.append(recommendation)
        flavors.remove(recommendation)
        like = input("喜欢这个口味吗？收藏它？(y/n)：")
        again = input("要再推荐一次吗？(y/n)：")
        if like.lower() == "y":
            if recommendation not in favorites:
                favorites.append(recommendation)
                print(f"❤️ 已收藏「{recommendation}」！")
            else:
                print("已经收藏过啦～")

        if again.lower() != "y":
            if history:
                print("\n📜 本次推荐历史：")
                for i, item in enumerate(history, 1):
                    print(f"  第{i}次：{item}")
                with open("history.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n【{name}的记录】\n")
                    for i, item in enumerate(history, 1):
                        f.write(f"  第{i}次：{item}\n")
                print("📁 已保存到 history.txt！")
            print("好的，祝你吃得开心！🍦")
            break

except ValueError:
    print("❌ 输入错误！请输入数字，例如：25 或 25.5")