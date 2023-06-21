import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()

app_dir = getattr(sys, '_MEIPASS', os.path.dirname(
    os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + app_dir


class UssGUI:
    def __init__(self):
        self.file_path = ""
        self.file_path_name = ""
        self.separate_level = ""

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("USS-GUI")

        # 添加选择文件按钮和文件路径输入框
        self.selectButton = tk.Button(self.root, text='选择文件', width=10, command=self.choose_file)
        self.selectButton.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.filePathEnrty = tk.Entry(self.root, width=35)
        self.filePathEnrty.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.filePathEnrty.insert(0, "请选择文件...")

        # 添加分离精细度复选框组
        self.v1 = tk.IntVar(value=0)
        self.v2 = tk.IntVar(value=0)
        self.v3 = tk.IntVar(value=0)
        self.levelGroup = tk.LabelFrame(self.root, text="请选择分离精细度")
        self.levelGroup.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.level1Button = tk.Checkbutton(self.levelGroup, text="LEVEL 1:最低精细度，可分离出人声，动物声，音乐...",
                                           variable=self.v1, onvalue=1, offvalue=0)
        self.level2Button = tk.Checkbutton(self.levelGroup, text="LEVEL 2:中等精细度，人群声，说话声，乐器声，车辆声...",
                                           variable=self.v2, onvalue=1, offvalue=0)
        self.level3Button = tk.Checkbutton(self.levelGroup, text="LEVEL 3:最高精细度，铃声，鸟声，管弦乐，打击乐...",
                                           variable=self.v3, onvalue=1, offvalue=0)
        self.level1Button.grid(row=3, column=0, sticky=tk.W)
        self.level2Button.grid(row=4, column=0, sticky=tk.W)
        self.level3Button.grid(row=5, column=0, sticky=tk.W)

        # 添加选择输出路径按钮和输出路径输入框
        self.exportButton = tk.Button(self.root, text="选择路径", width=10, command=self.choose_path)
        self.exportButton.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
        self.exportPathEntry = tk.Entry(self.root, width=35)
        self.exportPathEntry.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.exportPathEntry.insert(0, "请选择文件夹...")

        # 添加开始分离按钮和输出文本框
        self.startProcessButton = tk.Button(self.root, text='开始分离', width=35, command=self.start_process)
        self.startProcessButton.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        self.outputText = tk.Text(self.root, width=50, height=10)
        self.outputText.grid(row=9, column=0, columnspan=2)

        self.popup_window_toplevel = None

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_path_name = os.path.basename(self.file_path)
        file_name, file_ext = os.path.splitext(self.file_path_name)
        self.file_path_name = file_name  # 只保留文件名部分
        self.filePathEnrty.delete(0, tk.END)
        self.filePathEnrty.insert(0, self.file_path)
        return self.file_path

    def choose_path(self):
        self.path = filedialog.askdirectory()
        self.exportPathEntry.delete(0, tk.END)
        self.exportPathEntry.insert(0, self.path)

    def show_success_dialog(self, title, message):
        # 创建顶级窗口
        dialog = tk.Toplevel()
        dialog.title(title)

        # 创建标签控件来显示消息
        label = tk.Label(dialog, text=message)
        label.pack(padx=20, pady=20)

        # 创建按钮控件来关闭窗口
        button = tk.Button(dialog, text="关闭", command=dialog.destroy)
        button.pack(side=tk.BOTTOM, padx=20, pady=10)

        # 让窗口保持在最前面
        dialog.attributes('-topmost', True)

        # 窗口进入消息循环，等待用户操作
        dialog.mainloop()

    def start_process(self):
        self.outputText.delete('1.0', tk.END)  # 清空输出框

        if self.v1.get() == 1:
            self.separate_level += '1 '
        if self.v2.get() == 1:
            self.separate_level += '2 '
        if self.v3.get() == 1:
            self.separate_level += '3 '

        self.separate_level = self.separate_level.rstrip()

        levels = list(map(str, self.separate_level.strip().split()))

        def run_uss() -> None:

            python_path = os.path.join(app_dir, 'python3.8')
            inference_path = os.path.join(app_dir, 'inference.py')
            self.path = os.path.join(self.path, self.file_path_name)
            config_path = os.path.join(app_dir, 'ss_model=resunet30,querynet=at_soft,data=full.yaml')
            checkpoint_path = os.path.join(app_dir, 'pretrained.ckpt')

            uss_process = subprocess.Popen(
                [python_path, inference_path, '--audio_path', self.file_path, '--levels', *levels, '--output_dir', self.path, '--config_yaml', config_path,
                 '--checkpoint_path', checkpoint_path], stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

            # 循环读取uss程序的输出
            for line in iter(uss_process.stdout.readline, b''):
                # 将输出写入输出框中
                self.outputText.insert(tk.END, line.decode('utf-8'))
                # 滚动输出框以显示最新的内容
                self.outputText.see(tk.END)
                # 更新GUI界面
                self.outputText.update_idletasks()

            output, error = uss_process.communicate()
            if error:
                print(error.decode())
            print(output.decode())

            # 检查uss进程的退出代码
            return_code = uss_process.poll()
            if return_code != 0:
                error_message = f"分离错误： {return_code}"
                print(error_message)
                self.outputText.insert("end", error_message + "\n")
            else:
                success_message = "分离完成！"
                self.outputText.insert("end", success_message + "\n")

        # 创建新线程来运行uss命令
        thread = threading.Thread(target=run_uss)
        thread.start()

    def popup_window(self):
        # 创建Toplevel对象
        newWindow = tk.Toplevel(self.root)
        newWindow.title("文件导出")

        fileExportEntry = tk.Entry(newWindow, width=30)
        fileExportEntry.insert(0, "请选择导出路径...")
        fileExportEntry.grid(row=0, column=0, padx=5, pady=5)

        # 添加“浏览”按钮来选择导出路径
        def choose_export_path():
            export_path = filedialog.askdirectory()
            fileExportEntry.delete(0, tk.END)
            fileExportEntry.insert(0, export_path)

        browseButton = tk.Button(newWindow, text="浏览", width=10, command=choose_export_path)
        browseButton.grid(row=0, column=1, padx=5, pady=5)

        # 添加“导出”按钮来导出分离后的文件
        def export_files():
            if not os.path.exists(fileExportEntry.get()):
                os.mkdir(fileExportEntry.get())
            self.move_files_to_path(fileExportEntry.get())
            if self.popup_window_toplevel is not None and self.popup_window_toplevel.winfo_exists():
                self.popup_window_toplevel.destroy()

        exportButton = tk.Button(newWindow, text="导出", width=10, command=export_files)
        exportButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # 窗口进入消息循环，等待用户操作
        newWindow.mainloop()


# 创建UssGUI对象并启动主循环
gui = UssGUI()
gui.root.mainloop()