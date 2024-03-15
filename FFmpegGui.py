# -*- coding: GBK -*-
import sys
import time
import os
import time
import threading
import tkinter as tk
import tkinter.font as tkFont
import json
from tkinter import messagebox

from FFmpegServer import FFmpegServer

# 全局变量，记录文件上次修改时间
last_modified_time = None
log_rows = 100
open_loop = True
class FFmpegGui():

    def __init__(self, root):
        #setting title
        root.title("FFmpeg Gui Tool")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.radioValue = tk.StringVar(value='{"resolution":"1280x720","video_bitrate":"2000k","audio_sampling_rate":44100,"audio_bitrate":128}')

        self.GLabel_710=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_710["font"] = ft
        self.GLabel_710["fg"] = "#333333"
        self.GLabel_710["justify"] = "left"
        self.GLabel_710["text"] = "输入文件（文件/文件夹）："
        self.GLabel_710.place(x=10,y=30,width=154,height=30)

        self.GLineEdit_890=tk.Entry(root)
        self.GLineEdit_890["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_890["font"] = ft
        self.GLineEdit_890["fg"] = "#333333"
        self.GLineEdit_890["justify"] = "left"
        self.GLineEdit_890["text"] = ""
        self.GLineEdit_890.place(x=190,y=30,width=385,height=30)

        self.GButton_624=tk.Button(root)
        self.GButton_624["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.GButton_624["font"] = ft
        self.GButton_624["fg"] = "#333333"
        self.GButton_624["justify"] = "center"
        self.GButton_624["text"] = "开始转换"
        self.GButton_624.place(x=200,y=170,width=166,height=42)
        self.GButton_624["command"] = self.GButton_624_command

        self.GRadio_464=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GRadio_464["font"] = ft
        self.GRadio_464["fg"] = "#333333"
        self.GRadio_464["justify"] = "center"
        self.GRadio_464["text"] = "转码720P-2M"
        self.GRadio_464.place(x=90,y=120,width=95,height=30)
        self.GRadio_464["value"] = '{"resolution":"1280x720","video_bitrate":"2000k","audio_sampling_rate":44100,"audio_bitrate":128}'
        self.GRadio_464["command"] = self.GRadio_464_command
        self.GRadio_464["variable"] = self.radioValue

        self.GLabel_818=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_818["font"] = ft
        self.GLabel_818["fg"] = "#333333"
        self.GLabel_818["justify"] = "left"
        self.GLabel_818["text"] = "输出路径："
        self.GLabel_818.place(x=10,y=70,width=62,height=30)

        self.GLineEdit_615=tk.Entry(root)
        self.GLineEdit_615["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_615["font"] = ft
        self.GLineEdit_615["fg"] = "#333333"
        self.GLineEdit_615["justify"] = "left"
        self.GLineEdit_615["text"] = ""
        self.GLineEdit_615.place(x=190,y=70,width=386,height=30)

        self.GLabel_898=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_898["font"] = ft
        self.GLabel_898["fg"] = "#333333"
        self.GLabel_898["justify"] = "left"
        self.GLabel_898["text"] = "编码格式："
        self.GLabel_898.place(x=10,y=120,width=67,height=30)

        self.GRadio_490=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GRadio_490["font"] = ft
        self.GRadio_490["fg"] = "#333333"
        self.GRadio_490["justify"] = "center"
        self.GRadio_490["text"] = "转码720P-4M"
        self.GRadio_490.place(x=190,y=120,width=96,height=30)
        self.GRadio_490["value"] = '{"resolution":"1280x720","video_bitrate":"4000k","audio_sampling_rate":44100,"audio_bitrate":128}'
        self.GRadio_490["command"] = self.GRadio_490_command
        self.GRadio_490["variable"] = self.radioValue

        self.GRadio_244=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GRadio_244["font"] = ft
        self.GRadio_244["fg"] = "#333333"
        self.GRadio_244["justify"] = "center"
        self.GRadio_244["text"] = "转码1080P-2M"
        self.GRadio_244.place(x=300,y=120,width=97,height=30)
        self.GRadio_244["value"] = '{"resolution":"1920x1080","video_bitrate":"2000k","audio_sampling_rate":48000,"audio_bitrate":192}'
        self.GRadio_244["command"] = self.GRadio_244_command
        self.GRadio_244["variable"] = self.radioValue

        self.GRadio_814=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GRadio_814["font"] = ft
        self.GRadio_814["fg"] = "#333333"
        self.GRadio_814["justify"] = "center"
        self.GRadio_814["text"] = "转码1080P-4M"
        self.GRadio_814.place(x=410,y=120,width=97,height=30)
        self.GRadio_814["value"] = '{"resolution":"1920x1080","video_bitrate":"4000k","audio_sampling_rate":48000,"audio_bitrate":192}'
        self.GRadio_814["command"] = self.GRadio_814_command
        self.GRadio_814["variable"] = self.radioValue

        # 创建一个Scrollbar小部件
        self.GMessage_502=tk.Text(root,width=96,height=15)
        self.GMessage_502["bg"] = "#b5b5b5"
        ft = tkFont.Font(family='Times',size=10)
        self.GMessage_502["font"] = ft
        self.GMessage_502["fg"] = "#333333"
        self.GMessage_502.pack()
        self.GMessage_502.place(x=10,y=260)
        # self.GMessage_502.grid(row=8, column=10)

        self.GLabel_166=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_166["font"] = ft
        self.GLabel_166["fg"] = "#333333"
        self.GLabel_166["justify"] = "left"
        self.GLabel_166["text"] = "日志输出"
        self.GLabel_166.place(x=1,y=230,width=70,height=25)

        self.cb_val = tk.IntVar(value=1)
        self.GCheckBox_318 = tk.Checkbutton(root)
        ft = tkFont.Font(family='Times', size=10)
        self.GCheckBox_318["font"] = ft
        self.GCheckBox_318["fg"] = "#333333"
        self.GCheckBox_318["justify"] = "center"
        self.GCheckBox_318["text"] = "自动滚动日志"
        self.GCheckBox_318.place(x=470, y=230, width=107, height=30)
        self.GCheckBox_318["offvalue"] = "0"
        self.GCheckBox_318["onvalue"] = "1"
        self.GCheckBox_318["command"] = self.GCheckBox_318_command
        self.GCheckBox_318["variable"] = self.cb_val
        self.GCheckBox_318_command()

        # 创建事件对象
        self.event = threading.Event()
        self.log_name = 'ffmpeg-gui-tool.log'
        if not os.path.exists(self.log_name):
            with open(self.log_name,'w') as log:
                log.write('')
            log.close()
        # 创建线程1：检查文件是否有更新
        t1 = threading.Thread(target=self.check_file_update)
        t1.start()

        # 创建线程2：等待有更新后打印新内容
        t2 = threading.Thread(target=self.print_log)
        t2.start()



    def GButton_624_command(self):
        input_file = self.GLineEdit_890.get()
        output_path = self.GLineEdit_615.get()
        radio_val = self.radioValue.get()
        if not input_file:
            self.append_log('[ERROR]\t [输入地址不能为空！]')
            return
        if not output_path:
            self.append_log('[ERROR]\t [输出地址不能为空！]')
            return
        if not radio_val:
            self.append_log('[ERROR]\t [未选择编码格式！]')
            return
        self.modif_button_status(True)
        rvjson = json.loads(radio_val)
        resolution = rvjson.get('resolution')
        video_bitrate = rvjson.get('video_bitrate')
        audio_sampling_rate = rvjson.get('audio_sampling_rate')
        audio_bitrate = rvjson.get('audio_bitrate')
        ffmpegServer = FFmpegServer(self.append_log,self.append_log_row,self.modif_button_status)
        exec = threading.Thread(target=ffmpegServer.file_progress,args=(input_file, output_path, resolution, video_bitrate, audio_sampling_rate, audio_bitrate))
        exec.start()


    def modif_button_status(self,disabled):
        if disabled:
            self.GButton_624.config(state=tk.DISABLED, text="正在执行", bg="dark gray")
        else:
            self.GButton_624.config(state=tk.NORMAL, text="点击按钮", bg="#f0f0f0")

    def append_log(self,log):
        global log_rows
        self.GMessage_502.insert(tk.END, log+'\n')
        # 获取总行数
        total_lines = int(self.GMessage_502.index(tk.END).split('.')[0])
        # 如果总行数超过 100，则删除前面的行
        if total_lines > log_rows:
            # 删除前面的行，格式为 'line.column'
            self.GMessage_502.delete('1.0', f'{total_lines-log_rows+1}.0')

    def append_log_row(self, log):
        self.GMessage_502.insert(tk.END, log)
        total_lines = int(self.GMessage_502.index(tk.END).split('.')[0])
        if total_lines > log_rows:
            self.GMessage_502.delete('1.0', f'{total_lines-log_rows+1}.0')

    # 函数：检查文件是否有更新
    def check_file_update(self):
        global open_loop
        global last_modified_time
        while True:
            if open_loop:
                break
            # 获取文件的最后修改时间
            modified_time = os.path.getmtime(self.log_name)
            # 如果文件的最后修改时间发生了变化
            if modified_time != last_modified_time:
                last_modified_time = modified_time
                # 唤醒等待新内容的线程
                self.event.set()
            # 等待一段时间后再次检查文件是否有更新
            time.sleep(1)

    # 函数：等待有更新后打印新内容
    def print_log(self):
        global open_loop
        with open(self.log_name, 'r') as file:
            while True:
                if open_loop:
                    break
                file.flush()
                # 等待新内容的事件触发
                self.event.wait()
                # 读取文件内容并打印
                content = file.read()
                self.append_log(content)
                # 重置事件，继续等待新内容的事件触发
                self.event.clear()
    def GRadio_464_command(self):
        pass


    def GRadio_490_command(self):
        pass


    def GRadio_244_command(self):
        pass


    def GRadio_814_command(self):
        pass

    def GCheckBox_318_command(self):
        root.after(100,self.moveto_log)

    def moveto_log(self):
        if self.cb_val.get():
            self.GMessage_502.yview_moveto(1)
            root.after(100, self.moveto_log)
        else:
            self.GMessage_502.yview_moveto(0)

def on_closing():
    global open_loop
    if messagebox.askokcancel("退出", "是否要退出程序?"):
        open_loop = False
        root.quit()

root = tk.Tk()
app = FFmpegGui(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
# 监听关闭窗口事件
