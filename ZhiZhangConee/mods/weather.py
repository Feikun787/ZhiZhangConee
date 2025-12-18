import requests

class Weather:
    async def weather(self,msg,nub):
        text = None
        if msg.raw_message == "天气帮助":
            text = '格式：天气查询:省份:城市'
        if str(msg.raw_message).split(':')[0] == "天气查询":
            a = str(msg.raw_message).split(':')
            try:
                text = self.tianqi(a[1],a[2])
            except:
                text = '输入错误'
        if text:
            return {'try':'text',"text":text,'nub':nub}
    def tianqi(self,sheng, cheng):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

        a = f'https://i.news.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province={sheng}&city={cheng}&county='
        a = requests.get(a, headers=headers).json()
        a = dict(a)
        a = a['data']['forecast_24h']
        text = ''
        text += "天气信息摘要：\n"
        for weather_data in a:
            useful_info = {
                '日期': weather_data['time'],
                '白天天气': {
                    '天气状况': weather_data['day_weather'],
                    '温度范围': f"{weather_data['min_degree']}~{weather_data['max_degree']}°C",
                    '风向': weather_data['day_wind_direction'],
                    '风力': weather_data['day_wind_power']
                },
                '夜间天气': {
                    '天气状况': weather_data['night_weather'],
                    '风向': weather_data['night_wind_direction'],
                    '风力': weather_data['night_wind_power']
                },
                '空气质量': {
                    'AQI指数': weather_data['aqi'],
                    '等级': weather_data['aqi_name']
                }
            }

            # 打印整理后的信息
            text += f"日期: {useful_info['日期']}\n"
            text += "白天天气:\n"
            text += f"- 天气状况: {useful_info['白天天气']['天气状况']}\n"
            text += f"- 温度范围: {useful_info['白天天气']['温度范围']}\n"
            text += f"- 风向: {useful_info['白天天气']['风向']}\n"
            text += f"- 风力: {useful_info['白天天气']['风力']}级\n"

            text += "夜间天气:\n"
            text += f"- 天气状况: {useful_info['夜间天气']['天气状况']}\n"
            text += f"- 风向: {useful_info['夜间天气']['风向']}\n"
            text += f"- 风力: {useful_info['夜间天气']['风力']}级\n"

            text += "空气质量:\n"
            text += f"- AQI指数: {useful_info['空气质量']['AQI指数']}\n"
            text += f"- 等级: {useful_info['空气质量']['等级']}\n\n"
        return text