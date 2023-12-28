import hashlib
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime
from gc import collect
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from faker import Faker

font_path = "../data/font/yahei.ttf"
prop = fm.FontProperties(fname=font_path)

class CarData(object):
    """
    汽车用户数据生成：
        用户基本信息：
            用户id：基于MD5值生成
            姓名：基于faker随机生成
            身份证号：基于faker生成中国大陆身份证
            性别：男或女，整体符合均匀分布
            购车日期：从2010.1.1至2023.12.1范围内随机生成
            首次咨询日期：基于购车日期随机提前一段时间
            付款方式：贷款、全款
            职业：基于faker来随机生成
            城市：从河北省的所有地级市中随机选择，所有城市出现的频次要符合正态分布
            学历：从小学、初中、高中一直到博士、博士后，随机生成，所有学历按照频次要符合正态分布
            汽车保险金额：从3000至20000随机生成
            汽车保险品牌：从平安、泰康、人寿、太平洋等等中国大陆主流的保险公司随机选取，按照频次符合正态分布
        汽车基本信息：
            品牌：基于当前从懂车帝的汽车销售热榜来生成大致符合对应品牌排名与比例来生成对应品牌的数量
            型号：基于已有的品牌信息，来生成对应品牌下汽车的型号，例如品牌为沃尔沃，则型号可以是S60，S90，XC60，XC90等等
            配色：基于汽车常见的配色来随机生成
    """
    hebei_cities = ["石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊", "衡水", "雄安新区"]
    cities_p = [0.2, 0.1, 0.06, 0.04, 0.05, 0.13, 0.12, 0.08, 0.06, 0.1, 0.04, 0.02]
    educations = ["小学", "初中", "高中", "大专", "本科", "硕士", "博士", "博士后"]
    insure_companies = ["平安", "泰康", "人寿", "太平洋", "人保", "大地", "阳光", "新华"]
    car_brands_types = {
        "保时捷":[0.01, "macan", "卡宴", "718", "911", "帕拉梅拉", "taycan"],
        "北京":[0.03, "BJ40", "BJ60", "BJ80", "BJ90"],
        "沃尔沃":[0.06, "S60", "S90", "V60", "V90","XC40", "XC60", "XC90"],
        "奔驰":[0.02, "A200", "B200", "C260", "E300","S480", "GLC300", "GLB260", "GLE350", "CLA", "CLS"],
        "哈佛":[0.1, "H6", "H7", "H9", "哈佛大狗", "哈佛酷狗", "哈佛玉兔", "哈佛猛龙", "哈佛M6"],
        "红旗":[0.03, "H6", "H7", "H9", "HS", "H5", "HS5", "HS7", "HS9", "L5", "LS7"],
        "坦克":[0.06, "坦克300", "坦克400", "坦克500", "赛博坦克"],
        "比亚迪":[0.11, "秦", "汉DM", "元", "宋", "海豹", "汉EV", "秦plus"],
        "路虎":[0.01, "极光星脉", "卫士", "发现", "揽胜"],
        "吉利":[0.12, "星锐", "博越", "帝豪", "豪越", "星锐", "缤越"],
        "福特":[0.05, "福克斯", "蒙迪欧", "探险者", "领界"],
        "大众":[0.1, "迈腾", "速腾", "辉腾", "辉昂", "高尔夫", "宝来", "帕萨特", "途锐"],
        "宝马":[0.04, "118", "220", "330", "430", "530", "630", "730", "740"],
        "丰田":[0.03, "霸道", "亚洲龙", "皇冠", "雷凌", "凯美瑞", "汉兰达", "卡罗拉", "RAV4荣放", "亚州狮", "威驰"],
        "问界":[0.03, "M5", "M7", "M9"],
        "五菱汽车":[0.09, "五菱宏光", "mini", "五菱宾果"],
        "理想汽车":[0.01, "L7", "one", "L8", "L9"],
        "长安":[0.1, "cs55", "cs75", "cs75plus", "cs85", "cs95", "uni-v", "uni-k", "uni-t", "逸动", "cc"],
                        }
    car_colors = common_car_colors = [
        "黑色", "白色", "银灰色", "深灰色",
        "红色", "蓝色", "绿色", "黄色",
        "海岩灰", "香槟色", "橙色", "金色",
        "紫色", "粉色", "天蓝色", "深蓝色",
        "冰川白", "石英灰", "珍珠白", "午夜黑"
        ]
    fake = Faker("zh_CN")

    def __init__(self, data_num, save_path, save_name):
        """
        :param data_num: 需要生成的数据量，为整型
        :param save_path: 生成的数据存储的路径
        :param save_name: 生成的数据存储的文件名
        """
        self.data_num = data_num
        self.save_path = save_path
        self.save_name = save_name
    def categorydata_normal_generate(self, category_data, data_num, variance=1, plot=False):
        """
        给类别数据依据频次生成符合正态分布的数据，均值为len(category_data)
        :param category_data: 为给定的原始类别标签数据，按照从左到右元素的生成的频次从低到高，到最高再降低，左右两边形成对称正态分布
        :param data_num: 生成的数据量
        :param variance: 正态分布的方差
        :return: 正态分布的数据
        """
        # 生成符合正态分布的随机索引，是浮点数
        normal_dist_indices = np.random.normal(loc=len(category_data)/2, scale=variance, size=data_num)
        # 将生成的浮点数转换为整数，并设置在category_data有效索引范围内（a_min,a_max），
        # 所有整数符合正态分布，基于整数回溯找对应索引标签
        normal_dist_indices = np.clip(np.round(normal_dist_indices),
                                      a_min=0, a_max=len(category_data)-1).astype(int)
        normal_data = [category_data[index] for index in normal_dist_indices]
        normal_data_counts = Counter(normal_data)
        ordered_counts = [normal_data_counts[level] for level in category_data]
        if plot:
            # 绘制条形图
            plt.bar(category_data, ordered_counts)
            # 设置图表标题和坐标轴标签
            plt.title('Ordered Education Level Distribution')
            plt.xticks(fontproperties=prop)
            plt.xlabel('Education Level')
            plt.ylabel('Frequency')
        return normal_data
    def generate_md5_id(self, index):
        return hashlib.md5(str(index).encode()).hexdigest()
    def generate_data(self):
        data = pd.DataFrame()
        data["userid"] = [self.generate_md5_id(i) for i in range(self.data_num)]
        data["name"] = [self.fake.name() for i in range(self.data_num)]
        data["id_card"] = [self.fake.ssn(min_age=20, max_age=50) for i in range(self.data_num)]
        data["gender"] = np.random.choice(["男", "女"], size=self.data_num, p=[0.6, 0.4])
        data["pay_date"] = [self.fake.date_between_dates(date_start=datetime(2010, 12, 1),
                                                    date_end=datetime(2023, 12, 1)) for i in range(self.data_num)]
        random_days = [random.choice(range(0, 100)) for i in range(data.shape[0])]
        data["pay_date"] = data["pay_date"].astype("datetime64[ns]")
        data["first_consult_date"] = data["pay_date"] - pd.to_timedelta(random_days, unit="D")
        data["pay_method"] = np.random.choice(["全款", "贷款"], size=self.data_num, p=[0.32, 0.68])
        data["job"] = [self.fake.job() for i in range(self.data_num)]

        data["city"] = np.random.choice(self.hebei_cities, size=self.data_num, p=self.cities_p)
        data["education"] = self.categorydata_normal_generate(category_data=self.educations,
                                                         data_num=self.data_num)
        data["insure_amount"] = [random.choice(range(3000, 20001)) for i in range(self.data_num)]
        data["insure_company"] = self.categorydata_normal_generate(category_data=self.insure_companies,
                                                              data_num=self.data_num)
        car_brand_p = []
        list(map(lambda x:car_brand_p.append(x[0]), list(self.car_brands_types.values())))
        data["car_brand"] = np.random.choice(list(self.car_brands_types.keys()),
                                             size=self.data_num, p=car_brand_p)
        data["car_type"] = [random.choice(self.car_brands_types[b][1:]) for b in data["car_brand"]]
        data["car_color"] = self.categorydata_normal_generate(category_data=self.car_colors,
                                                         data_num=self.data_num)
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        data.to_csv(self.save_path + self.save_name, index=False)
        print("car_user_data:", str(round(sys.getsizeof(data) / 1024 / 1024, 2)) + "MB")



class customize_field_data(object):
    """
    用于根据用户需求生成某一领域相关的数据（当前主要用于生成结构化数据）
    用户的需求通过参数进行描述：
        1、列定义：
            1、列名
            2、列的类型
            3、列的属性值
                1、类别类型：给出需要出现的属性值种类，以及每种属性值需要的在整体数据中的占比比率，总比率之和为1
                    例如血型：A:0.2      B:0.3       AB:0.2     O:0.3
                    当不指定属性值的占比比率时，则每一种属性数量随机生成
                2、数值类型：给出上下限范围，选择需要的数据分布，默认为在上下限范围随机生成，可选择正态分布、均匀分布
                3、时间类型：给出需要生成的时间类型格式示例，以及时间的起始时间点，终止时间点
        2、数据量定义

    该数据为模拟生成数据，仅用于学习使用
    """
    support_types = ["整型", "小数类型", "类别类型", "时间类型", "id类型", "手机号", "姓名"]
    fake = Faker("zh-CN")
    def __init__(self, data_num, data_custom, save_path, save_name, sheet_name, data_format):
        """
        生成数据时，需要定义的属性
        :param data_num: 数据量
        :param data_custom: 数据生成的需求文档，是pandas的dataframe格式，可依据提供的模版与说明文档进行撰写，
        :param save_path: 数据存储路径
        :param save_name: 数据保存的文件名
        :param sheet_name: 当生成的数据保存为excel
        :param data_format: 数据保存时选择的数据格式，可选择csv、txt、tsv、excel等
        """
        self.data_num = data_num
        self.data_custom = data_custom
        self.save_path = save_path
        self.save_name = save_name
        self.sheet_name = sheet_name
        self.data_format = data_format

    def generate_data(self):
        data = pd.DataFrame()
        cust_cols = self.data_custom.columns
        for col in cust_cols:
            col_type = self.data_custom.loc["类型", col]
            col_type = col_type.strip()
            if col_type not in  self.support_types:
                raise TypeError(f"暂时不支持{self.data_custom.loc['类型', col]}数据生成，"
                                f"支持类型目录请参考:\n {self.support_types}\n"
                                f"请检查需要生成的数据类型名称是否与支持的类型目录对应类型名称完全匹配")
            if col_type in ["整型", "小数类型"]:
                col_range = list(map(lambda x: eval(x), self.data_custom.loc["范围", col].split("-")))
                col_distribute = self.data_custom.loc["数据分布", col]
                if col_distribute == "正态分布":
                    data[col] = np.random.normal(
                        loc=sum(col_range)/2,
                        scale=col_range[1],
                        size=self.data_num)
                    data[col] = np.clip(data[col], col_range[0], col_range[1])
                    if self.data_custom.loc["类型", col] == "整型":
                        data[col] = data[col].astype(int)
                    if self.data_custom.loc["类型", col] == "小数类型":
                        float_acc = self.data_custom.loc["精度", col]
                        if float_acc is np.nan:
                            data[col] = data[col].apply(lambda x:round(x, 1))
                        elif not isinstance(float_acc, int) or float_acc <= 0 or float_acc > 10:
                            raise TypeError("精度必须是正整数，请重新设置，且精度最高为10")
                        else:
                            data[col] = data[col].apply(lambda x: round(x, float_acc))
                elif col_distribute == "均匀分布":
                    data[col] = np.random.uniform(low=col_range[0],
                                                  high=col_range[1],
                                                  size=self.data_num)
                    if self.data_custom.loc["类型", col] == "整型":
                        data[col] = data[col].astype(int)
                    if self.data_custom.loc["类型", col] == "小数类型":
                        float_acc = self.data_custom.loc["精度", col]
                        if float_acc is np.nan:
                            data[col] = data[col].apply(lambda x: round(x, 1))
                        elif not isinstance(float_acc, int) or float_acc <= 0 or float_acc > 10:
                            raise TypeError("精度必须是正整数，请重新设置，且精度最高为10")
                        else:
                            data[col] = data[col].apply(lambda x: round(x, float_acc))
                # excel中没有填写值位置类型为np.nan
                elif not col_distribute or col_distribute is np.nan:
                    if self.data_custom.loc["类型", col] == "整型":
                        data[col] = random.choices(range(col_range[0], col_range[1]+1), k=self.data_num)
                    elif self.data_custom.loc["类型", col] == "小数类型":
                        data[col] = np.linspace(col_range[0], col_range[1], self.data_num)
                        float_acc = self.data_custom.loc["精度", col]
                        if float_acc is np.nan:
                            data[col] = data[col].apply(lambda x: round(x, 1))
                        elif not isinstance(float_acc, int) or float_acc <= 0 or float_acc > 10:
                            raise TypeError("精度必须是正整数，请重新设置，且精度最高为10")
                        else:
                            data[col] = data[col].apply(lambda x: round(x, float_acc))

                else:
                    raise TypeError(f"{self.data_custom.loc['类型', col]}"
                                    f"数据生成暂时不支持{col_distribute}，请核对后重新填写")
            elif col_type == "类别类型":
                col_attributes = self.data_custom.loc["属性值", col].split("-")
                col_attributes_p = self.data_custom.loc["属性值概率", col]
                if col_attributes_p is np.nan:
                    data[col] = random.choices(col_attributes, k=self.data_num)
                else:
                    col_attributes_p = col_attributes_p.split("-")
                    col_attributes_p = list(map(lambda x:eval(x), col_attributes_p))
                    data[col] = np.random.choice(col_attributes, size=self.data_num, p=col_attributes_p)
            elif col_type.lower() == "id类型":
                data[col] = [hashlib.md5(str(i).encode()).hexdigest() for i in range(self.data_num)]
            elif col_type == "手机号":
                data[col] = [self.fake.phone_number() for i in range(self.data_num)]
            elif col_type == "时间类型":
                start, end = self.data_custom.loc["开始时间", col], self.data_custom.loc["结束时间", col]
                start, end = re.findall(r'\d+', start), re.findall(r'\d+', end)
                start, end = [int(s) for s in start], [int(s) for s in end]
                # 通过元组的拆包，批量将参数按照位置喂给函数
                start, end = datetime(*start), datetime(*end)
                if start >= end:
                    raise ValueError("您设置的结束时间早于或等于开始时间，请重新设置")
                data[col] = [self.fake.date_time_between(start_date=start, end_date=end)
                             for i in range(self.data_num)]
            elif col_type == "姓名":
                data[col] = [self.fake.name() for i in range(self.data_num)]
        print("data use memory:", str(round(sys.getsizeof(data) / 1024 / 1024, 2)) + "MB")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        if self.data_format in ["csv", "tsv", "txt"]:
            data.to_csv(f"{self.save_path}{self.save_name}{self.data_num}.{self.data_format}", index=False)
        elif self.data_format.lower() == "excel":
            data.to_excel(f"{self.save_path}{self.save_name}{self.data_num}.xlsx",
                          sheet_name=self.sheet_name,
                          index=False)
        collect()




















