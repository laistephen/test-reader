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

        # 2. 快速排版工具列（模仿 Lookbook 頂部按鈕）
        toolbar = tk.Frame(self.root, bg="#2d2d2d", padx=5, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text=" 📖 一鍵智慧排版 ", command=self.format_current_text, bg="#005fb8", fg="white", bd=0, padx=8, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Label(toolbar, text=" | ", fg="gray", bg="#2d2d2d").pack(side=tk.LEFT, padx=3)
        tk.Button(toolbar, text=" ＋ 放大 ", command=self.font_larger, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text=" － 縮小 ", command=self.font_smaller, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)
        tk.Label(toolbar, text=" | ", fg="gray", bg="#2d2d2d").pack(side=tk.LEFT, padx=3)
        tk.Button(toolbar, text=" 💡 切換日/夜間護眼 ", command=self.toggle_theme, bg="#3c3c3c", fg="white", bd=0).pack(side=tk.LEFT, padx=2)

        # 3. 主閱讀文字區域與滾動條（支援自動換行 wrap=tk.WORD）
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            self.text_frame, 
            wrap=tk.WORD,  # 自動換行，絕不超出視窗範圍
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

        # 4. 狀態列
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
            self.text_area.config(bg="#fdfdfd", fg="#222222", insertbackground="black")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("文字檔 (*.txt)", "*.txt"), ("所有檔案 (*.*) *.*")]
        )
        if not file_path:
            return

        raw_content = self.read_text_file(file_path)
        if raw_content is not None:
            # 載入時自動執行智慧排版，還原整齊的小說格式
            formatted_content = self.auto_format_text(raw_content)
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, formatted_content)
            self.text_area.see("1.0")
            
            file_size_kb = os.path.getsize(file_path) / 1024
            self.root.title(f"Modern Lookbook - {os.path.basename(file_path)}")
            self.status_bar.config(text=f"已開啟並完成智慧排版: {file_path} (大小: {file_size_kb:.1f} KB)")

    def read_text_file(self, file_path):
        encodings = ['gbk', 'gb18030', 'utf-8', 'cp950']
        raw_data = None
        
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        text = None
        for enc in encodings:
            try:
                text = raw_data.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        if text is None:
            messagebox.showerror("錯誤", "無法辨識此檔案的編碼格式！")
            return None
        return text

    def auto_format_text(self, text):
        """
        核心排版引擎：
        1. 解決網路小說常見的「強制亂斷行」問題（把被切斷的同一段文字自動合併）。
        2. 自動幫每個段落開頭補上標準的兩個全形空格（首行縮排）。
        3. 保留章節標題與分隔線獨立一行。
        """
        lines = text.splitlines()
        paragraphs = []
        current_paragraph = ""

        for line in lines:
            line_str = line.strip()
            if not line_str:
                if current_paragraph:
                    paragraphs.append(self.finalize_paragraph(current_paragraph))
                    current_paragraph = ""
                continue

            # 判斷是否為章節標題、作者或分隔線（保留獨立一行）
            is_special_line = (
                line_str.startswith("===") or 
                line_str.startswith("---") or 
                line_str.startswith("《") or 
                ("第" in line_str and "章" in line_str) or
                ("作者" in line_str)
            )

            if is_special_line:
                if current_paragraph:
                    paragraphs.append(self.finalize_paragraph(current_paragraph))
                    current_paragraph = ""
                paragraphs.append(line_str)
            else:
                # 如果上一行結尾是完整標點符號，代表段落結束；否則視為同一段繼續合併
                if not current_paragraph:
                    current_paragraph = line_str
                else:
                    if current_paragraph.endswith(('。', '！', '？', '”', '」', '…', '～', '.', '!', '?')):
                        paragraphs.append(self.finalize_paragraph(current_paragraph))
                        current_paragraph = line_str
                    else:
                        current_paragraph += line_str

        if current_paragraph:
            paragraphs.append(self.finalize_paragraph(current_paragraph))

        return "\n\n".join(paragraphs)

    def finalize_paragraph(self, para):
        # 確保段落開頭有兩個全形空格縮排
        clean_para = para.replace(" ", "")
        if not clean_para.startswith("  "):
            clean_para = "  " + clean_para
        return clean_para

    def format_current_text(self):
        # 讓使用者隨時可以手動點擊按鈕重新排版目前畫面上的文字
        current_text = self.text_area.get(1.0, tk.END)
        formatted = self.auto_format_text(current_text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, formatted)
        self.text_area.see("1.0")
        self.status_bar.config(text="已執行一鍵智慧排版與首行縮排！")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBookReader(root)
    root.mainloop()