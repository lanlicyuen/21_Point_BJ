#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试多语言功能的脚本
"""

import tkinter as tk
from blackjack_counter import BlackjackCounter

def test_languages():
    """测试不同语言的界面文本"""
    
    print("测试多语言功能...")
    
    # 创建应用实例
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    app = BlackjackCounter(root)
    
    # 测试简体中文
    app.change_language('zh_CN')
    print(f"简体中文 - 标题: {app.get_text('title')}")
    print(f"简体中文 - 新局: {app.get_text('new_game')}")
    print(f"简体中文 - 关于: {app.get_text('about')}")
    
    # 测试繁体中文
    app.change_language('zh_TW')
    print(f"繁體中文 - 標題: {app.get_text('title')}")
    print(f"繁體中文 - 新局: {app.get_text('new_game')}")
    print(f"繁體中文 - 關於: {app.get_text('about')}")
    
    # 测试英文
    app.change_language('en')
    print(f"English - Title: {app.get_text('title')}")
    print(f"English - New Game: {app.get_text('new_game')}")
    print(f"English - About: {app.get_text('about')}")
    
    root.destroy()
    print("多语言功能测试完成！")

if __name__ == "__main__":
    test_languages()
