import random

def get_flavors(temperature, humidity):
    if temperature > 35:
        return "🥵 极热！清爽冰沙拯救你！", ["柠檬冰沙", "薄荷青柠", "椰子雪葩"]
    elif temperature > 30:
        if humidity < 50:
            return "🔥 干热天气，经典奶香最舒适！", ["牛奶", "香草", "草莓", "盐焦糖"]
        else:
            return "😮‍💨 闷热潮湿，来点清爽果味解腻！", ["荔枝玫瑰", "百香果", "西瓜雪葩"]
    elif temperature >= 25:
        if humidity < 60:
            return "😊 温暖舒适，果味奶味都很配！", ["草莓", "抹茶", "蓝莓"]
        else:
            return "🌫️ 有点闷，酸甜果味提提神！", ["柚子", "黄桃", "芒果"]
    elif temperature >= 15:
        return "🙂 温和天气，来点浓郁的！", ["巧克力", "榛果", "提拉米苏", "红豆"]
    elif temperature >= 5:
        return "🌥️ 有点凉，选暖心口味吧！", ["黑糖麻薯", "芋泥", "焦糖", "肉桂"]
    else:
        return "🥶 这么冷还吃冰？！钻被窝去！", []