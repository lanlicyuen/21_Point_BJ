import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class BlackjackCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("21点计牌器 by 1PLabs")
        self.root.geometry("870x540")
        self.root.configure(bg='#f0f0f0')
        
        # 数据文件路径
        self.data_file = "blackjack_data.json"
        
        # 初始化牌数据 (8副牌)
        self.cards = {
            'A': 32, '2': 32, '3': 32, '4': 32, '5': 32,
            '6': 32, '7': 32, '8': 32, '9': 32, '10': 32,
            'J': 32, 'Q': 32, 'K': 32
        }
        
        # 统计数据
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        
        # 语言设置
        self.current_language = 'zh_CN'  # 默认简体中文
        self.setup_translations()
        
        # 加载保存的数据
        self.load_data()
        
        self.setup_ui()
    
    def setup_translations(self):
        """设置多语言翻译"""
        self.translations = {
            'zh_CN': {  # 简体中文
                'title': '21点计牌器 by 1PLabs',
                'help': '帮助',
                'language': '语言',
                'about': '关于我',
                'new_game': '新局',
                'query': '查询',
                'save': '保存',
                'clear': '清除',
                'games_played': '已开局数',
                'win': 'Win',
                'lose': 'Lose',
                'result': '战果',
                'total_games': '总局数',
                'wins': '胜利',
                'losses': '失败',
                'win_rate': '胜率',
                'lose_rate': '负率',
                'used': '已用',
                'remaining': '剩余',
                'confirm': '确认',
                'success': '成功',
                'warning': '警告',
                'error': '错误',
                'data_query': '数据查询',
                'view_current': '查看当前数据',
                'view_saved': '查看保存的记录',
                'new_game_confirm': '确定要开始新局吗？这将重置所有牌数和统计数据。',
                'new_game_success': '新局已开始，所有数据已重置！',
                'clear_confirm': '确定要清除当前数据吗？这将重置所有牌数和统计数据但不会保存。',
                'clear_success': '数据已清除，界面已重置！',
                'win_lose_error': '胜利数和失败数的总和不能大于或等于总局数！请先增加局数。',
                'card_empty': ' 已经用完了！',
                'save_success': '当前记录已保存到文件: ',
                'about_text': '21点计牌器 by 1PLabs\n\n版本 v.1.0.1\n\n有问题有建议Email联系:\nlanlic@hotmail.com',
                'ok': '确定',
                'current_data': '当前游戏数据 - 查询时间: ',
                'card_stats': '=== 牌数统计 ===',
                'game_stats': '=== 游戏统计 ===',
                'deck_stats': '=== 牌组统计 ===',
                'total_cards': '总牌数',
                'used_cards': '已用牌数',
                'remaining_cards': '剩余牌数',
                'usage_rate': '使用率',
                'save_file_error': '保存记录失败: ',
                'read_file_error': '读取文件失败: ',
                'save_data_error': '保存数据失败: ',
                'load_data_error': '加载数据失败: ',
                'select_file_to_view': '选择要查看的记录文件',
                'select_file_to_delete': '选择要删除的记录文件',
                'confirm_delete': '确认删除',
                'delete_file_confirm': '确定要删除文件',
                'delete_success': '文件已删除',
                'delete_error': '删除文件失败: ',
                'saved_record': '保存的记录 - 文件: ',
                'save_time': '保存时间: ',
                'unknown_time': '未知'
            },
            'zh_TW': {  # 繁体中文
                'title': '21點計牌器 by 1PLabs',
                'help': '幫助',
                'language': '語言',
                'about': '關於我',
                'new_game': '新局',
                'query': '查詢',
                'save': '保存',
                'clear': '清除',
                'games_played': '已開局數',
                'win': 'Win',
                'lose': 'Lose',
                'result': '戰果',
                'total_games': '總局數',
                'wins': '勝利',
                'losses': '失敗',
                'win_rate': '勝率',
                'lose_rate': '負率',
                'used': '已用',
                'remaining': '剩餘',
                'confirm': '確認',
                'success': '成功',
                'warning': '警告',
                'error': '錯誤',
                'data_query': '數據查詢',
                'view_current': '查看當前數據',
                'view_saved': '查看保存的記錄',
                'new_game_confirm': '確定要開始新局嗎？這將重置所有牌數和統計數據。',
                'new_game_success': '新局已開始，所有數據已重置！',
                'clear_confirm': '確定要清除當前數據嗎？這將重置所有牌數和統計數據但不會保存。',
                'clear_success': '數據已清除，界面已重置！',
                'win_lose_error': '勝利數和失敗數的總和不能大於或等於總局數！請先增加局數。',
                'card_empty': ' 已經用完了！',
                'save_success': '當前記錄已保存到文件: ',
                'about_text': '21點計牌器 by 1PLabs\n\n版本 v.1.0.1\n\n有問題有建議Email聯繫:\nlanlic@hotmail.com',
                'ok': '確定',
                'current_data': '當前遊戲數據 - 查詢時間: ',
                'card_stats': '=== 牌數統計 ===',
                'game_stats': '=== 遊戲統計 ===',
                'deck_stats': '=== 牌組統計 ===',
                'total_cards': '總牌數',
                'used_cards': '已用牌數',
                'remaining_cards': '剩餘牌數',
                'usage_rate': '使用率',
                'save_file_error': '保存記錄失敗: ',
                'read_file_error': '讀取文件失敗: ',
                'save_data_error': '保存數據失敗: ',
                'load_data_error': '加載數據失敗: ',
                'select_file_to_view': '選擇要查看的記錄文件',
                'select_file_to_delete': '選擇要刪除的記錄文件',
                'confirm_delete': '確認刪除',
                'delete_file_confirm': '確定要刪除文件',
                'delete_success': '文件已刪除',
                'delete_error': '刪除文件失敗: ',
                'saved_record': '保存的記錄 - 文件: ',
                'save_time': '保存時間: ',
                'unknown_time': '未知'
            },
            'en': {  # English
                'title': 'Blackjack Counter by 1PLabs',
                'help': 'Help',
                'language': 'Language',
                'about': 'About',
                'new_game': 'New Game',
                'query': 'Query',
                'save': 'Save',
                'clear': 'Clear',
                'games_played': 'Games Played',
                'win': 'Win',
                'lose': 'Lose',
                'result': 'Results',
                'total_games': 'Total Games',
                'wins': 'Wins',
                'losses': 'Losses',
                'win_rate': 'Win Rate',
                'lose_rate': 'Loss Rate',
                'used': 'Used',
                'remaining': 'Remaining',
                'confirm': 'Confirm',
                'success': 'Success',
                'warning': 'Warning',
                'error': 'Error',
                'data_query': 'Data Query',
                'view_current': 'View Current Data',
                'view_saved': 'View Saved Records',
                'new_game_confirm': 'Start a new game? This will reset all card counts and statistics.',
                'new_game_success': 'New game started, all data has been reset!',
                'clear_confirm': 'Clear current data? This will reset all card counts and statistics without saving.',
                'clear_success': 'Data cleared, interface reset!',
                'win_lose_error': 'Total wins and losses cannot be greater than or equal to total games! Please increase game count first.',
                'card_empty': ' is out of cards!',
                'save_success': 'Current record saved to file: ',
                'about_text': 'Blackjack Counter by 1PLabs\n\nVersion v.1.0.1\n\nFor questions and suggestions:\nlanlic@hotmail.com',
                'ok': 'OK',
                'current_data': 'Current Game Data - Query Time: ',
                'card_stats': '=== Card Statistics ===',
                'game_stats': '=== Game Statistics ===',
                'deck_stats': '=== Deck Statistics ===',
                'total_cards': 'Total Cards',
                'used_cards': 'Used Cards',
                'remaining_cards': 'Remaining Cards',
                'usage_rate': 'Usage Rate',
                'save_file_error': 'Save record failed: ',
                'read_file_error': 'Read file failed: ',
                'save_data_error': 'Save data failed: ',
                'load_data_error': 'Load data failed: ',
                'select_file_to_view': 'Select record file to view',
                'select_file_to_delete': 'Select record file to delete',
                'confirm_delete': 'Confirm Delete',
                'delete_file_confirm': 'Are you sure to delete file',
                'delete_success': 'File deleted',
                'delete_error': 'Delete file failed: ',
                'saved_record': 'Saved Record - File: ',
                'save_time': 'Save Time: ',
                'unknown_time': 'Unknown'
            }
        }
    
    def get_text(self, key):
        """获取当前语言的文本"""
        return self.translations[self.current_language].get(key, key)
    
    def change_language(self, language):
        """切换语言"""
        self.current_language = language
        self.root.title(self.get_text('title'))
        # 重新构建界面
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def setup_ui(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.get_text('help'), menu=help_menu)
        
        # 语言子菜单
        language_menu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label=self.get_text('language'), menu=language_menu)
        language_menu.add_command(label="简体中文", command=lambda: self.change_language('zh_CN'))
        language_menu.add_command(label="繁體中文", command=lambda: self.change_language('zh_TW'))
        language_menu.add_command(label="English", command=lambda: self.change_language('en'))
        
        help_menu.add_separator()
        help_menu.add_command(label=self.get_text('about'), command=self.show_about)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部按钮区域
        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 新局按钮
        new_game_btn = tk.Button(top_frame, text=self.get_text('new_game'), font=('Arial', 12, 'bold'),
                                bg='#4CAF50', fg='white', width=10, height=2,
                                command=self.new_game)
        new_game_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 查询按钮
        query_btn = tk.Button(top_frame, text=self.get_text('query'), font=('Arial', 12, 'bold'),
                             bg='#2196F3', fg='white', width=10, height=2,
                             command=self.query_data)
        query_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 右侧功能按钮区域
        right_top_frame = tk.Frame(top_frame, bg='#f0f0f0')
        right_top_frame.pack(side=tk.RIGHT)
        
        # 保存按钮
        save_btn = tk.Button(right_top_frame, text=self.get_text('save'), font=('Arial', 12, 'bold'),
                            bg='#FF5722', fg='white', width=8, height=2,
                            command=self.save_current_record)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清除按钮
        clear_btn = tk.Button(right_top_frame, text=self.get_text('clear'), font=('Arial', 12, 'bold'),
                             bg='#9C27B0', fg='white', width=8, height=2,
                             command=self.clear_data)
        clear_btn.pack(side=tk.LEFT)
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧牌面按钮区域
        left_frame = tk.Frame(content_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        self.setup_card_buttons(left_frame)
        
        # 中间显示区域
        middle_frame = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=2)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        self.setup_middle_area(middle_frame)
        
        # 右侧统计区域
        right_frame = tk.Frame(content_frame, bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.setup_stats_area(right_frame)
    
    def setup_card_buttons(self, parent):
        """设置左侧牌面按钮"""
        card_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        for card in card_names:
            btn = tk.Button(parent, text=card, font=('Arial', 10, 'bold'),
                           width=3, height=1, bg='#e0e0e0',
                           command=lambda c=card: self.card_clicked(c))
            btn.pack(pady=(3, 2))
    
    def setup_middle_area(self, parent):
        """设置中间显示区域"""
        # 直接在父容器中创建显示区域，不使用滚动条
        self.scrollable_frame = tk.Frame(parent, bg='white')
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 5))
        
        self.update_card_display()
    
    def setup_stats_area(self, parent):
        """设置右侧统计区域"""
        # 已开局数
        games_label = tk.Label(parent, text=self.get_text('games_played'), font=('Arial', 12, 'bold'), bg='#f0f0f0')
        games_label.pack(pady=(0, 10))
        
        games_btn = tk.Button(parent, text="+1", font=('Arial', 12, 'bold'),
                             bg='#FF9800', fg='white', width=8, height=2,
                             command=self.increment_games)
        games_btn.pack(pady=(0, 5))
        
        # 防止双击
        games_btn.bind('<Double-Button-1>', lambda e: 'break')
        
        self.games_count_label = tk.Label(parent, text=str(self.games_played),
                                         font=('Arial', 14, 'bold'), fg='red', bg='#f0f0f0')
        self.games_count_label.pack(pady=(0, 20))
        
        # Win和Lose并排显示
        win_lose_frame = tk.Frame(parent, bg='#f0f0f0')
        win_lose_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Win区域
        win_frame = tk.Frame(win_lose_frame, bg='#f0f0f0')
        win_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        win_label = tk.Label(win_frame, text=self.get_text('win'), font=('Arial', 12, 'bold'), bg='#f0f0f0')
        win_label.pack(pady=(0, 5))
        
        win_btn = tk.Button(win_frame, text="+1", font=('Arial', 10, 'bold'),
                           bg='#4CAF50', fg='white', width=6, height=1,
                           command=self.increment_wins)
        win_btn.pack(pady=(0, 5))
        
        # 防止双击
        win_btn.bind('<Double-Button-1>', lambda e: 'break')
        
        self.wins_count_label = tk.Label(win_frame, text=str(self.wins),
                                        font=('Arial', 12, 'bold'), fg='red', bg='#f0f0f0')
        self.wins_count_label.pack()
        
        # Lose区域
        lose_frame = tk.Frame(win_lose_frame, bg='#f0f0f0')
        lose_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        lose_label = tk.Label(lose_frame, text=self.get_text('lose'), font=('Arial', 12, 'bold'), bg='#f0f0f0')
        lose_label.pack(pady=(0, 5))
        
        lose_btn = tk.Button(lose_frame, text="+1", font=('Arial', 10, 'bold'),
                            bg='#f44336', fg='white', width=6, height=1,
                            command=self.increment_losses)
        lose_btn.pack(pady=(0, 5))
        
        # 防止双击
        lose_btn.bind('<Double-Button-1>', lambda e: 'break')
        
        self.losses_count_label = tk.Label(lose_frame, text=str(self.losses),
                                          font=('Arial', 12, 'bold'), fg='red', bg='#f0f0f0')
        self.losses_count_label.pack()
        
        # 战果标题
        result_label = tk.Label(parent, text=self.get_text('result'), font=('Arial', 12, 'bold'), 
                               fg='red', bg='#f0f0f0')
        result_label.pack(pady=(10, 10))
        
        # 统计信息
        self.stats_text = tk.Text(parent, width=20, height=7, font=('Arial', 9),
                                 state=tk.DISABLED, bg='#f8f8f8')
        self.stats_text.pack(pady=(0, 10))
        
        self.update_stats_display()
    
    def update_card_display(self):
        """更新中间的牌数显示"""
        # 清除现有内容
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        card_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        for card in card_names:
            count = self.cards[card]
            # 创建每张牌的显示框架
            card_frame = tk.Frame(self.scrollable_frame, bg='white')
            card_frame.pack(fill=tk.X, padx=10, pady=(3, 2))
            
            # 牌名
            card_label = tk.Label(card_frame, text=f"{card}:", font=('Arial', 11, 'bold'),
                                 bg='white', width=3)
            card_label.pack(side=tk.LEFT)
            
            # 数量显示
            count_label = tk.Label(card_frame, text=f"{count}/32", font=('Arial', 11),
                                  bg='white', width=8)
            count_label.pack(side=tk.LEFT, padx=(5, 0))
            
            # 百分比
            percentage = (count / 32) * 100
            percent_label = tk.Label(card_frame, text=f"{percentage:.1f}%", 
                                   font=('Arial', 11), bg='white', width=8)
            percent_label.pack(side=tk.LEFT, padx=(5, 0))
            
            # 进度条
            progress_frame = tk.Frame(card_frame, bg='white')
            progress_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            progress = ttk.Progressbar(progress_frame, length=150, mode='determinate',
                                     style='green.Horizontal.TProgressbar')
            progress['value'] = percentage
            progress.pack(fill=tk.X)
    
    def card_clicked(self, card):
        """处理牌面按钮点击"""
        if self.cards[card] > 0:
            self.cards[card] -= 1
            self.update_card_display()
            self.save_data()
        else:
            messagebox.showwarning(self.get_text('warning'), f"{card}{self.get_text('card_empty')}")
    
    def increment_games(self):
        """增加已开局数"""
        self.games_played += 1
        self.games_count_label.config(text=str(self.games_played))
        self.update_stats_display()
        self.save_data()
    
    def increment_wins(self):
        """增加胜利数"""
        if self.wins + self.losses >= self.games_played:
            messagebox.showwarning(self.get_text('warning'), self.get_text('win_lose_error'))
            return
        self.wins += 1
        self.wins_count_label.config(text=str(self.wins))
        self.update_stats_display()
        self.save_data()
    
    def increment_losses(self):
        """增加失败数"""
        if self.wins + self.losses >= self.games_played:
            messagebox.showwarning(self.get_text('warning'), self.get_text('win_lose_error'))
            return
        self.losses += 1
        self.losses_count_label.config(text=str(self.losses))
        self.update_stats_display()
        self.save_data()
    
    def update_stats_display(self):
        """更新统计信息显示"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats_info = f"{self.get_text('total_games')}: {self.games_played}\n"
        stats_info += f"{self.get_text('wins')}: {self.wins}\n"
        stats_info += f"{self.get_text('losses')}: {self.losses}\n"
        
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            lose_rate = (self.losses / self.games_played) * 100
            stats_info += f"{self.get_text('win_rate')}: {win_rate:.1f}%\n"
            stats_info += f"{self.get_text('lose_rate')}: {lose_rate:.1f}%\n"
        
        # 计算剩余牌数
        total_remaining = sum(self.cards.values())
        total_cards = 13 * 32  # 13种牌 × 32张
        used_cards = total_cards - total_remaining
        
        stats_info += f"{self.get_text('used')}: {used_cards}\n"
        stats_info += f"{self.get_text('remaining')}: {total_remaining}\n"
        
        self.stats_text.insert(1.0, stats_info)
        self.stats_text.config(state=tk.DISABLED)
    
    def new_game(self):
        """开始新局，重置所有数据"""
        result = messagebox.askyesno(self.get_text('confirm'), self.get_text('new_game_confirm'))
        if result:
            # 重置牌数
            for card in self.cards:
                self.cards[card] = 32
            
            # 重置统计
            self.games_played = 0
            self.wins = 0
            self.losses = 0
            
            # 更新显示
            self.update_card_display()
            self.games_count_label.config(text="0")
            self.wins_count_label.config(text="0")
            self.losses_count_label.config(text="0")
            self.update_stats_display()
            
            # 保存数据
            self.save_data()
            messagebox.showinfo(self.get_text('success'), self.get_text('new_game_success'))
    
    def query_data(self):
        """查询数据功能 - 可以选择查看保存的记录文件"""
        query_window = tk.Toplevel(self.root)
        query_window.title(self.get_text('data_query'))
        query_window.geometry("600x500")
        query_window.configure(bg='#f0f0f0')
        
        # 按钮区域
        btn_frame = tk.Frame(query_window, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        # 查看当前数据按钮
        current_btn = tk.Button(btn_frame, text=self.get_text('view_current'), font=('Arial', 10, 'bold'),
                               bg='#2196F3', fg='white', width=15,
                               command=lambda: self.show_current_data(data_text))
        current_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 查看保存的记录按钮
        saved_btn = tk.Button(btn_frame, text=self.get_text('view_saved'), font=('Arial', 10, 'bold'),
                             bg='#FF9800', fg='white', width=15,
                             command=lambda: self.show_saved_records(data_text))
        saved_btn.pack(side=tk.LEFT)
        
        # 数据显示区域
        data_text = tk.Text(query_window, width=70, height=25, font=('Arial', 10))
        data_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # 默认显示当前数据
        self.show_current_data(data_text)
    
    def show_current_data(self, text_widget):
        """显示当前数据"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        # 构建查询结果
        query_result = f"{self.get_text('current_data')}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        query_result += f"{self.get_text('card_stats')}\n"
        
        for card, count in self.cards.items():
            percentage = (count / 32) * 100
            query_result += f"{card}: {count}/32 ({percentage:.1f}%)\n"
        
        query_result += f"\n{self.get_text('game_stats')}\n"
        query_result += f"{self.get_text('total_games')}: {self.games_played}\n"
        query_result += f"{self.get_text('wins')}: {self.wins}\n"
        query_result += f"{self.get_text('losses')}: {self.losses}\n"
        
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            lose_rate = (self.losses / self.games_played) * 100
            query_result += f"{self.get_text('win_rate')}: {win_rate:.1f}%\n"
            query_result += f"{self.get_text('lose_rate')}: {lose_rate:.1f}%\n"
        
        # 计算牌统计
        total_remaining = sum(self.cards.values())
        total_cards = 13 * 32
        used_cards = total_cards - total_remaining
        
        query_result += f"\n{self.get_text('deck_stats')}\n"
        query_result += f"{self.get_text('total_cards')}: {total_cards}\n"
        query_result += f"{self.get_text('used_cards')}: {used_cards}\n"
        query_result += f"{self.get_text('remaining_cards')}: {total_remaining}\n"
        query_result += f"{self.get_text('usage_rate')}: {(used_cards/total_cards)*100:.1f}%\n"
        
        text_widget.insert(1.0, query_result)
        text_widget.config(state=tk.DISABLED)
    
    def show_saved_records(self, text_widget):
        """显示保存的记录文件"""
        import tkinter.filedialog as filedialog
        
        # 选择要查看的文件
        filename = filedialog.askopenfilename(
            title=self.get_text('select_file_to_view'),
            filetypes=[("JSON files", "*.json")],
            initialdir="."
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                text_widget.config(state=tk.NORMAL)
                text_widget.delete(1.0, tk.END)
                
                # 显示保存的记录
                query_result = f"{self.get_text('saved_record')}{os.path.basename(filename)}\n"
                query_result += f"{self.get_text('save_time')}{data.get('save_time', self.get_text('unknown_time'))}\n\n"
                
                query_result += f"{self.get_text('card_stats')}\n"
                cards_data = data.get('cards', {})
                for card, count in cards_data.items():
                    percentage = (count / 32) * 100
                    query_result += f"{card}: {count}/32 ({percentage:.1f}%)\n"
                
                query_result += f"\n{self.get_text('game_stats')}\n"
                query_result += f"{self.get_text('total_games')}: {data.get('games_played', 0)}\n"
                query_result += f"{self.get_text('wins')}: {data.get('wins', 0)}\n"
                query_result += f"{self.get_text('losses')}: {data.get('losses', 0)}\n"
                
                stats = data.get('statistics', {})
                query_result += f"{self.get_text('win_rate')}: {stats.get('win_rate', 0):.1f}%\n"
                query_result += f"{self.get_text('lose_rate')}: {stats.get('lose_rate', 0):.1f}%\n"
                
                query_result += f"\n{self.get_text('deck_stats')}\n"
                query_result += f"{self.get_text('total_cards')}: {stats.get('total_cards', 416)}\n"
                query_result += f"{self.get_text('used_cards')}: {stats.get('used_cards', 0)}\n"
                query_result += f"{self.get_text('remaining_cards')}: {stats.get('remaining_cards', 416)}\n"
                query_result += f"{self.get_text('usage_rate')}: {(stats.get('used_cards', 0)/stats.get('total_cards', 416)*100):.1f}%\n"
                
                text_widget.insert(1.0, query_result)
                text_widget.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror(self.get_text('error'), f"{self.get_text('read_file_error')}{str(e)}")
    
    def save_data(self):
        """保存数据到文件"""
        data = {
            'cards': self.cards,
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'last_update': datetime.now().isoformat()
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror(self.get_text('error'), f"{self.get_text('save_data_error')}{str(e)}")
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.cards = data.get('cards', self.cards)
                self.games_played = data.get('games_played', 0)
                self.wins = data.get('wins', 0)
                self.losses = data.get('losses', 0)
                
            except Exception as e:
                messagebox.showerror(self.get_text('error'), f"{self.get_text('load_data_error')}{str(e)}")
    
    def save_current_record(self):
        """保存当前记录到带时间戳的JSON文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blackjack_record_{timestamp}.json"
        
        # 构建保存数据
        record_data = {
            'timestamp': timestamp,
            'save_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cards': self.cards.copy(),
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'statistics': {
                'total_cards': 13 * 32,
                'used_cards': (13 * 32) - sum(self.cards.values()),
                'remaining_cards': sum(self.cards.values()),
                'win_rate': (self.wins / self.games_played * 100) if self.games_played > 0 else 0,
                'lose_rate': (self.losses / self.games_played * 100) if self.games_played > 0 else 0
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(record_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo(self.get_text('success'), f"{self.get_text('save_success')}{filename}")
        except Exception as e:
            messagebox.showerror(self.get_text('error'), f"{self.get_text('save_file_error')}{str(e)}")
    
    def delete_current_record(self):
        """删除当前记录的文件选择"""
        import tkinter.filedialog as filedialog
        
        # 选择要删除的文件
        filename = filedialog.askopenfilename(
            title="选择要删除的记录文件",
            filetypes=[("JSON files", "*.json")],
            initialdir="."
        )
        
        if filename:
            try:
                # 确认删除
                result = messagebox.askyesno("确认删除", f"确定要删除文件 {os.path.basename(filename)} 吗？")
                if result:
                    os.remove(filename)
                    messagebox.showinfo("成功", f"文件 {os.path.basename(filename)} 已删除")
            except Exception as e:
                messagebox.showerror("错误", f"删除文件失败: {str(e)}")
    
    def clear_data(self):
        """清除当前数据，恢复到新局状态但不保存"""
        result = messagebox.askyesno(self.get_text('confirm'), self.get_text('clear_confirm'))
        if result:
            # 重置牌数
            for card in self.cards:
                self.cards[card] = 32
            
            # 重置统计
            self.games_played = 0
            self.wins = 0
            self.losses = 0
            
            # 更新显示
            self.update_card_display()
            self.games_count_label.config(text="0")
            self.wins_count_label.config(text="0")
            self.losses_count_label.config(text="0")
            self.update_stats_display()
            
            # 注意：这里不调用save_data()，所以不会保存到文件
            messagebox.showinfo(self.get_text('success'), self.get_text('clear_success'))
    
    def show_about(self):
        """显示关于信息"""
        about_window = tk.Toplevel(self.root)
        about_window.title(self.get_text('about'))
        about_window.geometry("300x200")
        about_window.configure(bg='#f0f0f0')
        about_window.resizable(False, False)
        
        # 居中显示窗口
        about_window.transient(self.root)
        about_window.grab_set()
        
        # 关于信息
        about_text = self.get_text('about_text')
        
        about_label = tk.Label(about_window, text=about_text, 
                              font=('Arial', 12), bg='#f0f0f0',
                              justify=tk.CENTER)
        about_label.pack(expand=True, pady=20)
        
        # 确定按钮
        ok_btn = tk.Button(about_window, text=self.get_text('ok'), font=('Arial', 10, 'bold'),
                          bg='#2196F3', fg='white', width=10,
                          command=about_window.destroy)
        ok_btn.pack(pady=(0, 20))

def main():
    root = tk.Tk()
    
    # 设置绿色进度条样式
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('green.Horizontal.TProgressbar',
                   troughcolor='#e0e0e0',
                   background='#4CAF50',
                   borderwidth=0)
    
    app = BlackjackCounter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
