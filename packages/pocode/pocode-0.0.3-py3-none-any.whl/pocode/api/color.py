# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
@代码日期    ：2023/12/23 22:54 
@本段代码的视频说明     ：
'''
import random

from colorama import init, Fore, Back, Style

init()  # 初始化Colorama模块


def single_color_print(text, background='RESET', foreground='RED', style='RESET_ALL'):
    background = getattr(Back, background)
    foreground = getattr(Fore, foreground)
    style = getattr(Style, style)
    print(background + foreground + text + style)


def random_color_print(text, background='RESET', foreground='RED', style='RESET_ALL'):
    background = getattr(Back, background)

    color_dict = {
                  "RED": "31",
                  "GREEN": "32",
                  "YELLOW": "33",
                  "BLUE": "34",
                  "MAGENTA": "35",
                  "CYAN": "36",
                  "WHITE": "37",
                  "RESET": "39"}
    random_color = random.choice(list(color_dict.keys()))
    foreground = getattr(Fore, random_color)
    style = getattr(Style, style)
    print(background + foreground + text + style)


if __name__ == '__main__':
    random_color_print(text="你好/小红书/公众号，都叫：程序员晚枫，www.python-office.com")
    random_color_print(text="你好/小红书/公众号，都叫：程序员晚枫，www.python-office.com")
    random_color_print(text="你好/小红书/公众号，都叫：程序员晚枫，www.python-office.com")
