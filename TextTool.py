import os
import chardet
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from opencc import OpenCC

class IntegratedConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("全能文件转换工具")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # 初始化现代感样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._init_styles()
        
        # 初始化变量
        self.function_var = tk.StringVar(value='encoding')
        self.input_folder = tk.StringVar()
        self.encoding_var = tk.StringVar(value='utf-8')
        self.conversion_var = tk.StringVar(value='t2s')

        self.create_widgets()

    def _init_styles(self):
        """初始化UI样式"""
        self.style.configure('TButton', padding=8, relief='flat', 
                           font=('微软雅黑', 10), background='#4CAF50')
        self.style.map('TButton',
                      background=[('active', '#45a049'), ('disabled', '#cccccc')])
        self.style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'), 
                           foreground='#2c3e50')
        self.style.configure('TFrame', background='#f0f3f5')
        self.style.configure('TRadiobutton', font=('微软雅黑', 9), 
                           background='#f0f3f5')
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TEntry', padding=5)

    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)

        # 功能选择区域
        func_frame = ttk.LabelFrame(main_frame, text=" 转换类型 ", padding=15)
        func_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=10)
        
        ttk.Radiobutton(func_frame, text="文本编码转换", variable=self.function_var,
                       value='encoding', command=self.toggle_interface).grid(row=0, column=0, padx=15)
        ttk.Radiobutton(func_frame, text="简繁体转换", variable=self.function_var,
                       value='conversion', command=self.toggle_interface).grid(row=0, column=1, padx=15)

        # 设置区域（动态切换）
        self.settings_frame = ttk.Frame(main_frame)
        self.settings_frame.grid(row=1, column=0, columnspan=3, pady=15, sticky='ew')

        # 编码转换设置
        self.encoding_panel = ttk.Frame(self.settings_frame)
        ttk.Label(self.encoding_panel, text="目标编码：").grid(row=0, column=0, padx=5)
        encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'utf-16']
        ttk.Combobox(self.encoding_panel, textvariable=self.encoding_var, 
                    values=encodings, width=18).grid(row=0, column=1)

        # 简繁体转换设置
        self.conversion_panel = ttk.Frame(self.settings_frame)
        ttk.Label(self.conversion_panel, text="转换方向：").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(self.conversion_panel, text="繁体→简体", variable=self.conversion_var,
                       value='t2s').grid(row=0, column=1, padx=10)
        ttk.Radiobutton(self.conversion_panel, text="简体→繁体", variable=self.conversion_var,
                       value='s2t').grid(row=0, column=2, padx=10)

        # 目录选择区域
        dir_frame = ttk.LabelFrame(main_frame, text=" 文件选择 ", padding=15)
        dir_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=10)
        
        ttk.Label(dir_frame, text="输入目录：").grid(row=0, column=0, padx=5)
        ttk.Entry(dir_frame, textvariable=self.input_folder, width=40).grid(row=0, column=1)
        ttk.Button(dir_frame, text="浏览目录", command=self.select_input_folder,
                  width=10).grid(row=0, column=2, padx=10)

        # 操作按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="开始转换", command=self.start_conversion,
                  style='TButton').grid(row=0, column=0, padx=15)
        ttk.Button(btn_frame, text="退出程序", command=self.root.destroy,
                  style='TButton').grid(row=0, column=1, padx=15)

        self.toggle_interface()

    def toggle_interface(self):
        """切换界面设置"""
        if self.function_var.get() == 'encoding':
            self.encoding_panel.pack(in_=self.settings_frame, anchor='w')
            self.conversion_panel.pack_forget()
        else:
            self.conversion_panel.pack(in_=self.settings_frame, anchor='w')
            self.encoding_panel.pack_forget()

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="选择输入目录")
        if folder:
            self.input_folder.set(folder)

    def start_conversion(self):
        input_dir = self.input_folder.get()
        if not input_dir:
            messagebox.showerror("错误", "请先选择输入目录！")
            return

        if self.function_var.get() == 'encoding':
            self.convert_encoding()
        else:
            self.convert_chinese()

    def convert_encoding(self):
        target_enc = self.encoding_var.get()
        try:
            converted, failed = self.batch_convert_encoding(
                input_dir=self.input_folder.get(),
                target_encoding=target_enc
            )
            messagebox.showinfo("完成", f"编码转换完成！\n成功：{converted} 个文件\n失败：{failed} 个文件")
        except Exception as e:
            messagebox.showerror("错误", f"编码转换失败：{str(e)}")

    def convert_chinese(self):
        try:
            cc = OpenCC(self.conversion_var.get())
            converted, failed = self.batch_convert_chinese(
                input_dir=self.input_folder.get(),
                output_dir=self.input_folder.get(),  # 使用相同目录覆盖原文件
                converter=cc
            )
            messagebox.showinfo("完成", f"简繁转换完成！\n成功：{converted} 个文件\n失败：{failed} 个文件")
        except Exception as e:
            messagebox.showerror("错误", f"简繁转换失败：{str(e)}")

    def batch_convert_encoding(self, input_dir, target_encoding, extensions=None):
        if extensions is None:
            extensions = ['.txt', '.csv', '.json', '.xml', '.html', '.htm', '.js', '.css', '.md']
        
        converted = 0
        failed = 0
        
        for root, _, files in os.walk(input_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    if self.single_convert_encoding(file_path, target_encoding):
                        converted += 1
                    else:
                        failed += 1
        return converted, failed

    def single_convert_encoding(self, file_path, target_encoding):
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()

            detected = chardet.detect(raw_data)
            source_encoding = detected['encoding'] if detected['confidence'] > 0.7 else None
            
            encodings_to_try = [
                source_encoding,
                'utf-8', 'gbk', 'gb2312', 'big5', 'latin1', 'utf-16',
                'iso-8859-1', 'cp1252'
            ]

            content = None
            for enc in encodings_to_try:
                if not enc: continue
                try:
                    content = raw_data.decode(enc)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue

            if not content:
                raise UnicodeDecodeError(f"无法解码文件: {file_path}")

            with open(file_path, 'w', encoding=target_encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"处理文件 {file_path} 出错: {str(e)}")
            return False

    def batch_convert_chinese(self, input_dir, output_dir, converter):
        converted = 0
        failed = 0
        
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        converted_content = converter.convert(content)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(converted_content)
                        converted += 1
                    except Exception as e:
                        print(f"转换失败：{file_path} - {str(e)}")
                        failed += 1
        return converted, failed

if __name__ == "__main__":
    app = IntegratedConverterApp()
    app.root.mainloop()