import tkinter as tk
from tkinter import filedialog, messagebox
import os

class ModernBookReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Lookbook - 專屬小說閱讀器")
        self.root.geometry("1000x800")

        self.font_size = 14
        self.is_dark_mode = True

        self.create_widgets()

    def create_widgets(self):
        # 1. 上方功能選單
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="開啟小說 (.txt)", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="離開", command=self.root.quit)
        menubar.add_cascade(label="檔案", menu=file_menu)
        
        # 排版選單
        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="一鍵智慧排版（段落重排/自動縮排）", command=self.format_current_text)
        menubar.add_cascade(label="排版相關", menu=format_menu)
        
        self.root.config(menu=menubar)

        # 2. 快捷鍵
        self.root.bind("<Control-o>", lambda event: self.open_file())

        # 3. 快速排版工具列
        toolbar = tk.Frame(self.root, bg="#2d2d2d", padx=5, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text=" 📖 一鍵智慧排版 ", command=self.format_current_text, bg="#005fb8", fg="white", bd=0, padx=8, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Label(toolbar, text=" | ", fg="gray", bg="#2d2d2d").pack(side=tk.LEFT, padx=3)
        tk.Button(toolbar, text=" ＋ 放大 ", command=self.font_larger, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=" － 縮小 ", command=self.font_smaller, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)
        tk.Label(toolbar, text=" | ", fg="gray", bg="#2d2d2d").pack(side=tk.LEFT, padx=3)
        tk.Button(toolbar, text=" 💡 切換日/夜間護眼 ", command=self.toggle_theme, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)

        # 4. 主閱讀文字區域與滾動條
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            self.text_frame, 
            wrap=tk.WORD, 
            yscrollcommand=self.scrollbar.set, 
            font=("微軟正黑體", self.font_size),
            bg="#1e1e1e",  # 護眼暗色背景
            fg="#d4d4d4",  # 柔和文字顏色
            insertbackground="white",
            padx=12,
            pady=12
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_area.yview)

        # 5. 狀態列
        self.status_bar = tk.Label(self.root, text="就緒 - 請點選 檔案 -> 開啟小說", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def font_larger(self):
        if self.font_size < 32:
            self.font_size += 2
            self.text_area.config(font=("微軟正黑體", self.font_size))

    def font_smaller(self):
        if self.font_size > 10:
            self.font_size -= 2
            self.text_area.config(font=("微軟正黑體", self.font_size))

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.text_area.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        else:
            self
