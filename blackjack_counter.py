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
        
        # 加载保存的数据
        self.load_data()
        
        self.setup_ui()
    
    def setup_ui(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于我", command=self.show_about)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部按钮区域
        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 新局按钮
        new_game_btn = tk.Button(top_frame, text="新局", font=('Arial', 12, 'bold'),
                                bg='#4CAF50', fg='white', width=10, height=2,
                                command=self.new_game)
        new_game_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 查询按钮
        query_btn = tk.Button(top_frame, text="查询", font=('Arial', 12, 'bold'),
                             bg='#2196F3', fg='white', width=10, height=2,
                             command=self.query_data)
        query_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 右侧功能按钮区域
        right_top_frame = tk.Frame(top_frame, bg='#f0f0f0')
        right_top_frame.pack(side=tk.RIGHT)
        
        # 保存按钮
        save_btn = tk.Button(right_top_frame, text="保存", font=('Arial', 12, 'bold'),
                            bg='#FF5722', fg='white', width=8, height=2,
                            command=self.save_current_record)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清除按钮
        clear_btn = tk.Button(right_top_frame, text="清除", font=('Arial', 12, 'bold'),
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
        games_label = tk.Label(parent, text="已开局数", font=('Arial', 12, 'bold'), bg='#f0f0f0')
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
        
        win_label = tk.Label(win_frame, text="Win", font=('Arial', 12, 'bold'), bg='#f0f0f0')
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
        
        lose_label = tk.Label(lose_frame, text="Lose", font=('Arial', 12, 'bold'), bg='#f0f0f0')
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
        result_label = tk.Label(parent, text="战果", font=('Arial', 12, 'bold'), 
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
            messagebox.showwarning("警告", f"{card} 已经用完了！")
    
    def increment_games(self):
        """增加已开局数"""
        self.games_played += 1
        self.games_count_label.config(text=str(self.games_played))
        self.update_stats_display()
        self.save_data()
    
    def increment_wins(self):
        """增加胜利数"""
        if self.wins + self.losses >= self.games_played:
            messagebox.showwarning("警告", "胜利数和失败数的总和不能大于或等于总局数！请先增加局数。")
            return
        self.wins += 1
        self.wins_count_label.config(text=str(self.wins))
        self.update_stats_display()
        self.save_data()
    
    def increment_losses(self):
        """增加失败数"""
        if self.wins + self.losses >= self.games_played:
            messagebox.showwarning("警告", "胜利数和失败数的总和不能大于或等于总局数！请先增加局数。")
            return
        self.losses += 1
        self.losses_count_label.config(text=str(self.losses))
        self.update_stats_display()
        self.save_data()
    
    def update_stats_display(self):
        """更新统计信息显示"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats_info = f"总局数: {self.games_played}\n"
        stats_info += f"胜利: {self.wins}\n"
        stats_info += f"失败: {self.losses}\n"
        
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            lose_rate = (self.losses / self.games_played) * 100
            stats_info += f"胜率: {win_rate:.1f}%\n"
            stats_info += f"负率: {lose_rate:.1f}%\n"
        
        # 计算剩余牌数
        total_remaining = sum(self.cards.values())
        total_cards = 13 * 32  # 13种牌 × 32张
        used_cards = total_cards - total_remaining
        
        stats_info += f"已用: {used_cards}\n"
        stats_info += f"剩余: {total_remaining}\n"
        
        self.stats_text.insert(1.0, stats_info)
        self.stats_text.config(state=tk.DISABLED)
    
    def new_game(self):
        """开始新局，重置所有数据"""
        result = messagebox.askyesno("确认", "确定要开始新局吗？这将重置所有牌数和统计数据。")
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
            messagebox.showinfo("成功", "新局已开始，所有数据已重置！")
    
    def query_data(self):
        """查询数据功能 - 可以选择查看保存的记录文件"""
        query_window = tk.Toplevel(self.root)
        query_window.title("数据查询")
        query_window.geometry("600x500")
        query_window.configure(bg='#f0f0f0')
        
        # 按钮区域
        btn_frame = tk.Frame(query_window, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        # 查看当前数据按钮
        current_btn = tk.Button(btn_frame, text="查看当前数据", font=('Arial', 10, 'bold'),
                               bg='#2196F3', fg='white', width=15,
                               command=lambda: self.show_current_data(data_text))
        current_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 查看保存的记录按钮
        saved_btn = tk.Button(btn_frame, text="查看保存的记录", font=('Arial', 10, 'bold'),
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
        query_result = f"当前游戏数据 - 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        query_result += "=== 牌数统计 ===\n"
        
        for card, count in self.cards.items():
            percentage = (count / 32) * 100
            query_result += f"{card}: {count}/32 ({percentage:.1f}%)\n"
        
        query_result += f"\n=== 游戏统计 ===\n"
        query_result += f"总局数: {self.games_played}\n"
        query_result += f"胜利数: {self.wins}\n"
        query_result += f"失败数: {self.losses}\n"
        
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            lose_rate = (self.losses / self.games_played) * 100
            query_result += f"胜率: {win_rate:.1f}%\n"
            query_result += f"负率: {lose_rate:.1f}%\n"
        
        # 计算牌统计
        total_remaining = sum(self.cards.values())
        total_cards = 13 * 32
        used_cards = total_cards - total_remaining
        
        query_result += f"\n=== 牌组统计 ===\n"
        query_result += f"总牌数: {total_cards}\n"
        query_result += f"已用牌数: {used_cards}\n"
        query_result += f"剩余牌数: {total_remaining}\n"
        query_result += f"使用率: {(used_cards/total_cards)*100:.1f}%\n"
        
        text_widget.insert(1.0, query_result)
        text_widget.config(state=tk.DISABLED)
    
    def show_saved_records(self, text_widget):
        """显示保存的记录文件"""
        import tkinter.filedialog as filedialog
        
        # 选择要查看的文件
        filename = filedialog.askopenfilename(
            title="选择要查看的记录文件",
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
                query_result = f"保存的记录 - 文件: {os.path.basename(filename)}\n"
                query_result += f"保存时间: {data.get('save_time', '未知')}\n\n"
                
                query_result += "=== 牌数统计 ===\n"
                cards_data = data.get('cards', {})
                for card, count in cards_data.items():
                    percentage = (count / 32) * 100
                    query_result += f"{card}: {count}/32 ({percentage:.1f}%)\n"
                
                query_result += f"\n=== 游戏统计 ===\n"
                query_result += f"总局数: {data.get('games_played', 0)}\n"
                query_result += f"胜利数: {data.get('wins', 0)}\n"
                query_result += f"失败数: {data.get('losses', 0)}\n"
                
                stats = data.get('statistics', {})
                query_result += f"胜率: {stats.get('win_rate', 0):.1f}%\n"
                query_result += f"负率: {stats.get('lose_rate', 0):.1f}%\n"
                
                query_result += f"\n=== 牌组统计 ===\n"
                query_result += f"总牌数: {stats.get('total_cards', 416)}\n"
                query_result += f"已用牌数: {stats.get('used_cards', 0)}\n"
                query_result += f"剩余牌数: {stats.get('remaining_cards', 416)}\n"
                query_result += f"使用率: {(stats.get('used_cards', 0)/stats.get('total_cards', 416)*100):.1f}%\n"
                
                text_widget.insert(1.0, query_result)
                text_widget.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {str(e)}")
    
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
            messagebox.showerror("错误", f"保存数据失败: {str(e)}")
    
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
                messagebox.showerror("错误", f"加载数据失败: {str(e)}")
    
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
            messagebox.showinfo("成功", f"当前记录已保存到文件: {filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存记录失败: {str(e)}")
    
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
        result = messagebox.askyesno("确认清除", "确定要清除当前数据吗？这将重置所有牌数和统计数据但不会保存。")
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
            messagebox.showinfo("成功", "数据已清除，界面已重置！")
    
    def show_about(self):
        """显示关于信息"""
        about_window = tk.Toplevel(self.root)
        about_window.title("关于我")
        about_window.geometry("300x200")
        about_window.configure(bg='#f0f0f0')
        about_window.resizable(False, False)
        
        # 居中显示窗口
        about_window.transient(self.root)
        about_window.grab_set()
        
        # 关于信息
        about_text = "21点计牌器 by 1PLabs\n\n版本 v.1.0\n\n有问题有建议Email联系:\nlanlic@hotmail.com"
        
        about_label = tk.Label(about_window, text=about_text, 
                              font=('Arial', 12), bg='#f0f0f0',
                              justify=tk.CENTER)
        about_label.pack(expand=True, pady=20)
        
        # 确定按钮
        ok_btn = tk.Button(about_window, text="确定", font=('Arial', 10, 'bold'),
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
