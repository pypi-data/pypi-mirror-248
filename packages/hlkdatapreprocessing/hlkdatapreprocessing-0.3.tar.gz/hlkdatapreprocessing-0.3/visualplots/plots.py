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


def bar_plot(bar_x, bar_y,
             fig_x=8, fig_y=6, fg_dpi=80, cust_font=None,
             xt_fontsize=10, xt_rotation=0,
             yt_fontsize=10, yt_rotation=0,
             text_size=10,
             title="", tit_fontsize=10, tit_y=1.1,
             xlabel="", xl_fontsize=10, xl_x=1.0, xl_ratation=0,
             ylabel="", yl_fontsize=10, yl_x=1.0, yl_ratation=0):
    """
    绘制竖直方向条形统计图
    :param bar_x: 条形统计图的x轴数据
    :param bar_y: 条形统计图的y轴数据
    :param fig_x: 绘图的画布尺寸的长,单位为英寸，默认为8
    :param fig_y: 绘图的画布尺寸的宽,单位为英寸，默认为6
    :param fg_dpi: 绘制的图的像素，默认为80
    :param cust_font: 自定义字体，当涉及中文相关字体时，需要导入中文字体可正常显示
          （通过matplotlib的font_manager，fm.FontProperties(fname=font_path)导入）
    :param xt_fontsize: x坐标轴上的字体大小，默认为10
    :param xt_rotation: x坐标轴上的字的旋转角度，默认为0
    :param yt_fontsize: y坐标轴上的字体大小，默认为10
    :param yt_rotation: y坐标轴上的字的旋转角度，默认为0
    :param text_size: 图中每个柱子的数据标签字体大小
    :param title: 图名标题，默认为空
    :param tit_fontsize: 图名标题字体的大小，默认为10
    :param tit_y: 图名标题字体相对于图的高度，默认为1.1
    :param xlabel: x坐标轴含义标签，默认为空
    :param xl_fontsize: x坐标轴含义标签字体大小，默认为10
    :param xl_x: x坐标轴含义标签字体位置，默认为1.0，表示将标签设置在右下角
    :param xl_ratation: x坐标轴含义标签字体旋转角度，默认为0
    :param ylabel:  y坐标轴含义标签，默认为空
    :param yl_fontsize: y坐标轴含义标签字体大小，默认为10
    :param yl_x: y坐标轴含义标签字体位置，默认为1.0，表示将标签设置在左上角
    :param yl_ratation: y坐标轴含义标签字体旋转角度，默认为0
    :return: 无返回值
    """
    plt.figure(figsize=(fig_x, fig_y), dpi=fg_dpi)
    plt.bar(x=bar_x, height=bar_y)
    plt.xticks(bar_x, fontproperties=cust_font, fontsize=xt_fontsize, rotation=xt_rotation)
    plt.yticks(fontproperties=cust_font, fontsize=yt_fontsize, rotation=yt_rotation)
    for i, v in enumerate(bar_y):
        plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=text_size)
    plt.title(title, fontproperties=cust_font, fontsize=tit_fontsize, y=tit_y)
    plt.xlabel(xlabel, fontproperties=cust_font, fontsize=xl_fontsize, x=xl_x, rotation=xl_ratation)
    plt.ylabel(ylabel, fontproperties=cust_font, fontsize=yl_fontsize, y=yl_x, rotation=yl_ratation)
    plt.show()

# print(help(customize_field_data))