import datetime

class ChineseCalendar:
    # 天干地支对照表
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 生肖对照表
    SHENGXIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    
    # 五行对照表
    WUXING_TIANGAN = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火",
        "戊": "土", "己": "土", "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    WUXING_DIZHI = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    # 时辰地支对照表（23-1点为子时）
    HOUR_DIZHI = [
        ("子", 23, 1), ("丑", 1, 3), ("寅", 3, 5), ("卯", 5, 7),
        ("辰", 7, 9), ("巳", 9, 11), ("午", 11, 13), ("未", 13, 15),
        ("申", 15, 17), ("酉", 17, 19), ("戌", 19, 21), ("亥", 21, 23)
    ]
    
    # 六十甲子表
    JIAZI_TABLE = []
    
    def __init__(self):
        self._generate_jiazi_table()
    
    def _generate_jiazi_table(self):
        """生成六十甲子表"""
        self.JIAZI_TABLE = []
        gan_idx, zhi_idx = 0, 0
        for i in range(60):
            self.JIAZI_TABLE.append(self.TIANGAN[gan_idx] + self.DIZHI[zhi_idx])
            gan_idx = (gan_idx + 1) % 10
            zhi_idx = (zhi_idx + 1) % 12
    
    def get_year_ganzhi(self, year):
        """计算年柱"""
        # 以公元4年为甲子年基准
        base_year = 4
        offset = (year - base_year) % 60
        return self.JIAZI_TABLE[offset]

    def get_month_ganzhi(self, year_ganzhi, month):
        """计算月柱"""
        year_gan = year_ganzhi[0]
        # 月支：寅月为正月，对应地支索引
        month_zhi_index = (month + 1) % 12
        month_dizhi = self.DIZHI[month_zhi_index]

        # 根据年干确定月干起始位置
        year_index = self.TIANGAN.index(year_gan)
        # 月干公式：年干索引×2 + 月份
        month_gan_index = (year_index * 2 + month) % 10
        month_gan = self.TIANGAN[month_gan_index]

        return month_gan + month_dizhi

    def get_day_ganzhi(self, year, month, day):
        """计算日柱 - 使用公式法"""
        # 以1900年1月31日为基准日（甲子日）
        # 简化计算：使用蔡勒公式变体
        if month < 3:
            year -= 1
            month += 12

        # 使用简化公式计算日干支序号
        Y = year
        M = month
        D = day

        # 公元纪年简化计算公式
        # 基础值为1900年1月31日（甲子日）
        base_days = (1900 - 1) * 365 + (1900 - 1) // 4 - (1900 - 1) // 100 + (1900 - 1) // 400
        target_days = (Y - 1) * 365 + (Y - 1) // 4 - (Y - 1) // 100 + (Y - 1) // 400
        target_days += (306 * (M + 1)) // 10 + D - 62

        days_diff = target_days - base_days
        ganzhi_index = days_diff % 60

        return self.JIAZI_TABLE[ganzhi_index]

    def get_hour_ganzhi(self, day_ganzhi, hour):
        """计算时柱"""
        # 确定时辰地支
        hour_dizhi = None
        for dizhi, start, end in self.HOUR_DIZHI:
            if start == 23:  # 处理子时的特殊情况
                if hour >= 23 or hour < 1:
                    hour_dizhi = dizhi
                    break
            elif hour >= start and hour < end:
                hour_dizhi = dizhi
                break
        
        if hour_dizhi is None:
            hour_dizhi = "子"
        
        # 根据日干确定时干
        day_gan = day_ganzhi[0]
        day_index = self.TIANGAN.index(day_gan)
        
        # 时干计算公式：日干索引×2 + 时辰地支索引
        hour_zhi_index = self.DIZHI.index(hour_dizhi)
        hour_gan_index = (day_index * 2 + hour_zhi_index) % 10
        hour_gan = self.TIANGAN[hour_gan_index]
        
        return hour_gan + hour_dizhi
    
    def get_wuxing(self, ganzhi):
        """获取干支对应的五行"""
        if len(ganzhi) != 2:
            return ""
        
        gan = ganzhi[0]
        zhi = ganzhi[1]
        
        gan_wuxing = self.WUXING_TIANGAN.get(gan, "")
        zhi_wuxing = self.WUXING_DIZHI.get(zhi, "")
        
        return f"{gan_wuxing}{zhi_wuxing}"
    
    def get_shengxiao(self, year):
        """获取生肖"""
        offset = (year - 4) % 12
        return self.SHENGXIAO[offset]
    
    def get_nayin(self, ganzhi):
        """获取纳音五行"""
        nayin_map = {
            "甲子": "海中金", "乙丑": "海中金",
            "丙寅": "炉中火", "丁卯": "炉中火",
            "戊辰": "大林木", "己巳": "大林木",
            "庚午": "路旁土", "辛未": "路旁土",
            "壬申": "剑锋金", "癸酉": "剑锋金",
            "甲戌": "山头火", "乙亥": "山头火",
            "丙子": "涧下水", "丁丑": "涧下水",
            "戊寅": "城头土", "己卯": "城头土",
            "庚辰": "白蜡金", "辛巳": "白蜡金",
            "壬午": "杨柳木", "癸未": "杨柳木",
            "甲申": "泉中水", "乙酉": "泉中水",
            "丙戌": "屋上土", "丁亥": "屋上土",
            "戊子": "霹雳火", "己丑": "霹雳火",
            "庚寅": "松柏木", "辛卯": "松柏木",
            "壬辰": "长流水", "癸巳": "长流水",
            "甲午": "砂石金", "乙未": "砂石金",
            "丙申": "山下火", "丁酉": "山下火",
            "戊戌": "平地木", "己亥": "平地木",
            "庚子": "壁上土", "辛丑": "壁上土",
            "壬寅": "金箔金", "癸卯": "金箔金",
            "甲辰": "覆灯火", "乙巳": "覆灯火",
            "丙午": "天河水", "丁未": "天河水",
            "戊申": "大驿土", "己酉": "大驿土",
            "庚戌": "钗钏金", "辛亥": "钗钏金",
            "壬子": "桑柘木", "癸丑": "桑柘木",
            "甲寅": "大溪水", "乙卯": "大溪水",
            "丙辰": "沙中土", "丁巳": "沙中土",
            "戊午": "天上火", "己未": "天上火",
            "庚申": "石榴木", "辛酉": "石榴木",
            "壬戌": "大海水", "癸亥": "大海水"
        }
        return nayin_map.get(ganzhi, "未知")

class EightCharactersCalculator:
    def __init__(self):
        self.calendar = ChineseCalendar()
    
    def calculate_bazi(self, year, month, day, hour, minute=0):
        """
        计算八字
        :param year: 年（公历）
        :param month: 月（1-12）
        :param day: 日（1-31）
        :param hour: 时（0-23）
        :param minute: 分（0-59）
        :return: 八字信息字典
        """
        try:
            # 验证日期有效性
            datetime.date(year, month, day)
        except ValueError:
            return {"error": "无效的日期"}
        
        # 计算年柱
        year_ganzhi = self.calendar.get_year_ganzhi(year)
        
        # 计算月柱（简化版，未考虑节气）
        month_ganzhi = self.calendar.get_month_ganzhi(year_ganzhi, month)
        
        # 计算日柱
        day_ganzhi = self.calendar.get_day_ganzhi(year, month, day)
        
        # 计算时柱
        hour_ganzhi = self.calendar.get_hour_ganzhi(day_ganzhi, hour)
        
        # 计算五行
        year_wuxing = self.calendar.get_wuxing(year_ganzhi)
        month_wuxing = self.calendar.get_wuxing(month_ganzhi)
        day_wuxing = self.calendar.get_wuxing(day_ganzhi)
        hour_wuxing = self.calendar.get_wuxing(hour_ganzhi)
        
        # 计算生肖
        shengxiao = self.calendar.get_shengxiao(year)
        
        # 计算纳音
        year_nayin = self.calendar.get_nayin(year_ganzhi)
        month_nayin = self.calendar.get_nayin(month_ganzhi)
        day_nayin = self.calendar.get_nayin(day_ganzhi)
        hour_nayin = self.calendar.get_nayin(hour_ganzhi)
        
        # 统计五行数量
        all_wuxing = year_wuxing + month_wuxing + day_wuxing + hour_wuxing
        wuxing_count = {
            "金": all_wuxing.count("金"),
            "木": all_wuxing.count("木"),
            "水": all_wuxing.count("水"),
            "火": all_wuxing.count("火"),
            "土": all_wuxing.count("土")
        }
        
        return {
            "birth_date": f"{year}年{month}月{day}日 {hour}时{minute}分",
            "bazi": {
                "年柱": year_ganzhi,
                "月柱": month_ganzhi,
                "日柱": day_ganzhi,
                "时柱": hour_ganzhi
            },
            "wuxing": {
                "年柱五行": year_wuxing,
                "月柱五行": month_wuxing,
                "日柱五行": day_wuxing,
                "时柱五行": hour_wuxing
            },
            "nayin": {
                "年柱纳音": year_nayin,
                "月柱纳音": month_nayin,
                "日柱纳音": day_nayin,
                "时柱纳音": hour_nayin
            },
            "shengxiao": shengxiao,
            "wuxing_count": wuxing_count,
            "wuxing_balance": self._analyze_wuxing_balance(wuxing_count)
        }
    
    def _analyze_wuxing_balance(self, wuxing_count):
        """分析五行平衡"""
        total = sum(wuxing_count.values())
        if total == 0:
            return "五行数据异常"
        
        balance_info = []
        for element, count in wuxing_count.items():
            percentage = (count / total) * 100
            if count == 0:
                balance_info.append(f"{element}：缺失")
            elif percentage < 15:
                balance_info.append(f"{element}：偏弱({percentage:.1f}%)")
            elif percentage > 25:
                balance_info.append(f"{element}：偏强({percentage:.1f}%)")
            else:
                balance_info.append(f"{element}：适中({percentage:.1f}%)")
        
        return balance_info
    
    def print_bazi_report(self, bazi_data):
        """打印八字报告"""
        if "error" in bazi_data:
            print(f"错误：{bazi_data['error']}")
            return
        
        print("=" * 60)
        print("                  八字五行分析报告")
        print("=" * 60)
        print(f"出生时间：{bazi_data['birth_date']}")
        print(f"生    肖：{bazi_data['shengxiao']}")
        print()
        
        print("【四柱八字】")
        print("-" * 40)
        for pillar, ganzhi in bazi_data['bazi'].items():
            wuxing = bazi_data['wuxing'][pillar + "五行"]
            nayin = bazi_data['nayin'][pillar + "纳音"]
            print(f"  {pillar}：{ganzhi}  |  五行：{wuxing}  |  纳音：{nayin}")
        
        print()
        print("【五行统计】")
        print("-" * 40)
        for element, count in bazi_data['wuxing_count'].items():
            bar = "█" * count + " " * (4 - count)
            print(f"  {element}: {count}个  {bar}")
        
        print()
        print("【五行平衡分析】")
        print("-" * 40)
        for item in bazi_data['wuxing_balance']:
            print(f"  {item}")
        
        print()
        print("【日主分析】")
        print("-" * 40)
        self._analyze_day_master(bazi_data)
        
        print("=" * 60)

    def print_bazi_report2(self, bazi_data):
        """打印八字报告"""
        text = """"""
        if "error" in bazi_data:
            return f"错误：{bazi_data['error']}"
            return

        text +="=" * 10+"\n"
        text +="        八字五行分析报告\n"
        text +="=" * 10+"\n"
        text +=f"出生时间：{bazi_data['birth_date']}\n"
        text +=f"生    肖：{bazi_data['shengxiao']}\n"
        text +="\n"

        text +="【四柱八字】\n"
        text +="-" * 10+"\n"
        for pillar, ganzhi in bazi_data['bazi'].items():
            wuxing = bazi_data['wuxing'][pillar + "五行"]
            nayin = bazi_data['nayin'][pillar + "纳音"]
            text +=f"{pillar}：{ganzhi}|五行：{wuxing}|纳音：{nayin}\n"

        text +="\n"
        text +="【五行统计】\n"
        text +=("-" * 10+"\n")
        for element, count in bazi_data['wuxing_count'].items():
            bar = "█" * count + " " * (4 - count)
            text +=f"  {element}: {count}个  {bar}\n"

        text +="\n"
        text +="【五行平衡分析】\n"
        text +="-" * 10+"\n"
        for item in bazi_data['wuxing_balance']:
            text +=f"  {item}\n"

        text +="\n"
        text +="【日主分析】\n"
        text +="-" * 10+"\n"
        text+=self._analyze_day_master2(bazi_data)

        text +=("=" * 10)
        return text

    def _analyze_day_master2(self, bazi_data):
        """分析日主（日干）"""
        text = """"""
        day_gan = bazi_data['bazi']['日柱'][0]
        day_gan_wuxing = self.calendar.WUXING_TIANGAN[day_gan]

        text +=f"  日主（日干）：{day_gan} ({day_gan_wuxing})\n"
        text +=f"  代表命主自身，属{day_gan_wuxing}性\n"

        # 简单的生克关系
        shengke_map = {
            "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
            "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
            "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"},
            "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
            "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"}
        }

        if day_gan_wuxing in shengke_map:
            relations = shengke_map[day_gan_wuxing]
            text += f"  生（助我）：{relations['被生']} → 生{day_gan_wuxing}\n"
            text +=f"  克（我助）：{day_gan_wuxing} → 生{relations['生']}\n"
            text +=f"  被克（克我）：{relations['被克']} → 克{day_gan_wuxing}"
            text +=f"  被生（我克）：{day_gan_wuxing} → 克{relations['克']}\n"

        # 分析日主强弱（简化版）
        day_wuxing_count = bazi_data['wuxing_count'][day_gan_wuxing]
        total_wuxing = sum(bazi_data['wuxing_count'].values())
        day_percentage = (day_wuxing_count / total_wuxing) * 100

        text +=f"\n  日主{day_gan_wuxing}在八字中占比：{day_percentage:.1f}%\n"
        if day_percentage < 15:
            text +="  日主偏弱，可能需要生扶\n"
        elif day_percentage > 25:
            text +="  日主偏强，可能需要克制\n"
        else:
            text +="  日主力量适中\n"
        return  text
    
    def _analyze_day_master(self, bazi_data):
        """分析日主（日干）"""
        day_gan = bazi_data['bazi']['日柱'][0]
        day_gan_wuxing = self.calendar.WUXING_TIANGAN[day_gan]
        
        print(f"  日主（日干）：{day_gan} ({day_gan_wuxing})")
        print(f"  代表命主自身，属{day_gan_wuxing}性")
        
        # 简单的生克关系
        shengke_map = {
            "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
            "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
            "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"},
            "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
            "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"}
        }
        
        if day_gan_wuxing in shengke_map:
            relations = shengke_map[day_gan_wuxing]
            print(f"  生（助我）：{relations['被生']} → 生{day_gan_wuxing}")
            print(f"  克（我助）：{day_gan_wuxing} → 生{relations['生']}")
            print(f"  被克（克我）：{relations['被克']} → 克{day_gan_wuxing}")
            print(f"  被生（我克）：{day_gan_wuxing} → 克{relations['克']}")
        
        # 分析日主强弱（简化版）
        day_wuxing_count = bazi_data['wuxing_count'][day_gan_wuxing]
        total_wuxing = sum(bazi_data['wuxing_count'].values())
        day_percentage = (day_wuxing_count / total_wuxing) * 100
        
        print(f"\n  日主{day_gan_wuxing}在八字中占比：{day_percentage:.1f}%")
        if day_percentage < 15:
            print("  日主偏弱，可能需要生扶")
        elif day_percentage > 25:
            print("  日主偏强，可能需要克制")
        else:
            print("  日主力量适中")

def main():
    """主函数"""
    calculator = EightCharactersCalculator()
    
    print("八字五行计算程序")
    print("=" * 60)
    
    while True:
        try:
            print("\n请输入出生信息（输入q退出）")
            
            year_input = input("出生年份（公历，如1990）：")
            if year_input.lower() == 'q':
                break
            year = int(year_input)
            
            month = int(input("出生月份（1-12）："))
            day = int(input("出生日期（1-31）："))
            
            hour_input = input("出生时辰（0-23，如不确定请输入12）：")
            hour = int(hour_input) if hour_input else 12
            
            print("\n正在计算，请稍候...")
            print()
            
            # 计算八字
            bazi_data = calculator.calculate_bazi(year, month, day, hour)
            
            # 打印报告
            calculator.print_bazi_report(bazi_data)
            
            # 保存结果选项
            save_option = input("\n是否保存结果到文件？(y/n): ")
            if save_option.lower() == 'y':
                filename = f"bazi_{year}_{month}_{day}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("八字五行分析报告\n")
                    f.write("=" * 60 + "\n")
                    f.write(f"出生时间：{bazi_data['birth_date']}\n")
                    f.write(f"生肖：{bazi_data['shengxiao']}\n\n")
                    
                    f.write("【四柱八字】\n")
                    f.write("-" * 40 + "\n")
                    for pillar, ganzhi in bazi_data['bazi'].items():
                        wuxing = bazi_data['wuxing'][pillar + "五行"]
                        nayin = bazi_data['nayin'][pillar + "纳音"]
                        f.write(f"  {pillar}：{ganzhi}  |  五行：{wuxing}  |  纳音：{nayin}\n")
                    
                    f.write("\n【五行统计】\n")
                    f.write("-" * 40 + "\n")
                    for element, count in bazi_data['wuxing_count'].items():
                        bar = "█" * count + " " * (4 - count)
                        f.write(f"  {element}: {count}个  {bar}\n")
                    
                    f.write("\n【五行平衡分析】\n")
                    f.write("-" * 40 + "\n")
                    for item in bazi_data['wuxing_balance']:
                        f.write(f"  {item}\n")
                
                print(f"结果已保存到 {filename}")
            
            continue_option = input("\n是否继续计算？(y/n): ")
            if continue_option.lower() != 'y':
                break
                
        except ValueError as e:
            print(f"输入错误：请输入正确的数字")
        except Exception as e:
            print(f"计算过程中出现错误：{e}")

def test_examples():
    """测试示例"""
    calculator = EightCharactersCalculator()
    
    print("八字计算程序测试示例")
    print("=" * 60)
    
    # 测试几个已知的八字
    test_cases = [
        ("1990年1月1日12时", 1990, 1, 1, 12),
        ("2000年8月8日8时", 2000, 8, 8, 8),
        ("1984年2月2日0时", 1984, 2, 2, 0),
        ("2023年12月31日23时", 2023, 12, 31, 23),
    ]
    
    for desc, year, month, day, hour in test_cases:
        print(f"\n测试案例：{desc}")
        print("-" * 40)
        try:
            bazi_data = calculator.calculate_bazi(year, month, day, hour)
            print(f"八字：{bazi_data['bazi']['年柱']} {bazi_data['bazi']['月柱']} {bazi_data['bazi']['日柱']} {bazi_data['bazi']['时柱']}")
            print(f"生肖：{bazi_data['shengxiao']}")
            print(f"日主：{bazi_data['bazi']['日柱'][0]} ({calculator.calendar.WUXING_TIANGAN[bazi_data['bazi']['日柱'][0]]})")
        except Exception as e:
            print(f"计算错误：{e}")


def main2(sr):
    """主函数"""
    calculator = EightCharactersCalculator()

    year_input = str(sr).split('.')[0]
    year = int(year_input)

    month = int(str(sr).split('.')[1])
    day = int(str( sr).split('.')[2])

    hour_input = str(sr).split('.')[3]
    hour = int(hour_input) if hour_input else 12


            # 计算八字
    bazi_data = calculator.calculate_bazi(year, month, day, hour)

            # 打印报告
    text = calculator.print_bazi_report2(bazi_data)
    return text





if __name__ == "__main__":
    # 显示测试示例
    test_option = input("是否查看测试示例？(y/n): ")
    if test_option.lower() == 'y':
        test_examples()
    
    # 运行主程序
    run_main = input("\n是否开始计算您的八字？(y/n): ")
    if run_main.lower() == 'y':
        print(main2("2005.06.13.11")
    )
    print("\n程序结束，感谢使用！")