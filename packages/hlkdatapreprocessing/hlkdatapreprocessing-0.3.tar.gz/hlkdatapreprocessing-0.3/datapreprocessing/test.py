import pandas as pd
from data_generate import customize_field_data

cust = pd.read_excel("../data/data_generate_requirements/汽车数据生成.xlsx", sheet_name=["汽车销售数据"])
cust = cust["汽车销售数据"]
cust.index = cust["数据信息"]
cust = cust.drop(["数据信息"], axis=1)
customize_field_data(
    data_num=10000,
    data_custom=cust,
    save_path="../data/generate/generated_data/汽车数据/",
    save_name="汽车销售",
    sheet_name="汽车销售数据",
    data_format="csv",
).generate_data()
