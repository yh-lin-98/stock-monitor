import time
import datetime
from pytdx.hq import TdxHq_API


# 简单的实时数据获取
def simple_get_data():
    api = TdxHq_API()

    with api.connect('60.191.117.167', 7709):
        # 获取指定股票的实时价格
        stock_list = [(1, '688802')]  # (市场, 股票代码)
        quotes = api.get_security_quotes(stock_list)

        print("实时价格数据:")
        for quote in quotes:
            print(f"股票: {quote['code']}")
            print(f"  当前价: {quote['price']}")
            print(f"  昨收: {quote['last_close']}")
            print(f"  今开: {quote['open']}")
            print(f"  最高: {quote['high']}")
            print(f"  最低: {quote['low']}")
            print(f"  成交量: {quote['vol']}")
            print(f"  涨跌幅: {((quote['price'] - quote['last_close']) / quote['last_close'] * 100):.2f}%")

        # 获取分时数据
        minute_data = api.get_minute_time_data(1, '688802')
        print(f"\n分时数据 (最近5条):")
        if minute_data:
            for data in minute_data[-5:]:
                print(f"时间: {data}")
                # print(f"  {data['datetime']} - 价格: {data['price']}, 成交量: {data['vol']}")


# 持续获取版本
def continuous_get_data(interval_minutes=30, total_hours=24):
    """
    持续获取数据并打印

    :param interval_minutes: 获取间隔（分钟）
    :param total_hours: 总监控时长（小时）
    """
    total_iterations = int(total_hours * 60 / interval_minutes)

    for i in range(total_iterations):
        current_time = datetime.datetime.now()
        print(f"\n[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] 获取数据...")

        api = TdxHq_API()
        if api.connect('60.191.117.167', 7709):
            # 获取实时价格
            quotes = api.get_security_quotes([(1, '688802')])
            if quotes:
                quote = quotes[0]
                print(
                    f"股票: {quote['code']}, 当前价: {quote['price']}, 涨跌幅: {((quote['price'] - quote['last_close']) / quote['last_close'] * 100):.2f}%")

            # 获取分时数据
            minute_data = api.get_minute_time_data(1, '688802')
            if minute_data:
                latest = minute_data[-1]
                print(f"最新分时: {latest['datetime']}, 价格: {latest['price']}, 成交量: {latest['vol']}")

            api.disconnect()
        else:
            print("连接失败")

        # 等待下次获取
        if i < total_iterations - 1:
            print(f"等待 {interval_minutes} 分钟...")
            time.sleep(interval_minutes * 60)


# 运行示例
simple_get_data()
# continuous_get_data(interval_minutes=30, total_hours=2)  # 每30分钟获取一次，持续2小时
