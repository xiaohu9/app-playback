# 对录制的脚本文件进行回放
import time
import re
from PyQt5.QtCore import QThread
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController


# 用于回放多个事件
class Playback(QThread):
    def __init__(self, filelist, text=None):
        super(Playback, self).__init__()
        self.files = filelist
        self.isrunning = True
        self.text = text  # 用于回放时在文本框中显示信息

    # 运行回放事件
    def run(self):
        time.sleep(3)
        if self.text is not None:
            self.text.printf("回放开始")
        else:
            print("回放开始")
        for file in self.files:
            self.playback_single(file)

    # 停止回放事件
    def stop(self):
        # 回放标志位设置为False
        self.isrunning = False

    # 回放单个事件
    def playback_single(self, file):
        if self.text is not None:
            self.text.printf("当前回放文件：" + file)
        else:
            print("当前回放文件：" + file)
        with open(file, 'r') as f:
            timestmp = 0
            for line in f:
                if not self.isrunning:
                    if self.text is not None:
                        self.text.printf("回放停止")
                    else:
                        print("回放中断")
                    break
                if timestmp != 0:
                    timeB = float(line.split(" ")[0])  # 获取当前操作时间戳
                    time.sleep(timeB - timestmp)  # 休眠时间戳差值

                if "Mouse" in line:
                    mode = re.compile(r"(\d+) (\d+)")  # 正则匹配鼠标坐标
                    res = re.search(mode, line)  # 匹配结果
                    if res:
                        # 获取鼠标坐标
                        x = res.group(1)
                        y = res.group(2)
                        mouse = MouseController()
                        mouse.position = (x, y)
                        if "clicked" in line:
                            if "Left" in line:
                                mouse.press(Button.left)
                                if self.text is not None:
                                    self.text.printf("鼠标左键按下: {0}, {1}".format(x, y))
                                else:
                                    print("鼠标左键按下: {0}, {1}".format(x, y))
                            elif "Middle" in line:
                                mouse.press(Button.middle)
                                if self.text is not None:
                                    self.text.printf("鼠标中键按下: {0}, {1}".format(x, y))
                                else:
                                    print("鼠标中键按下: {0}, {1}".format(x, y))
                            elif "Right" in line:
                                mouse.press(Button.right)
                                if self.text is not None:
                                    self.text.printf("鼠标右键按下: {0}, {1}".format(x, y))
                                else:
                                    print("鼠标右键按下: {0}, {1}".format(x, y))
                            else:
                                if self.text is not None:
                                    self.text.printf("press 未知的鼠标按键")
                                else:
                                    print("press 未知的鼠标按键")
                        elif "released" in line:
                            if "Left" in line:
                                mouse.release(Button.left)
                                if self.text is not None:
                                    self.text.printf("鼠标左键释放: {0}, {1}".format(x, y))
                                else:
                                    print("鼠标左键释放: {0}, {1}".format(x, y))
                            elif "Middle" in line:
                                mouse.release(Button.middle)
                                if self.text is not None:
                                    self.text.printf("鼠标中键释放: {0}, {1}".format(x, y))
                                else:
                                    print("鼠标中键释放: {0}, {1}".format(x, y))
                            elif "Right" in line:
                                mouse.release(Button.right)
                            else:
                                if self.text is not None:
                                    self.text.printf("release 未知的鼠标按键")
                                else:
                                    print("release 未知的鼠标按键")
                    else:
                        if self.text is not None:
                            self.text.printf("鼠标正则匹配失败")
                        else:
                            print("鼠标正则匹配失败")
                elif "Key" in line:
                    keyboard = KeyboardController()
                    if "char" in line:
                        mode = re.compile(r"char (.+?) ")  # 正则匹配键盘普通按键
                        res = re.search(mode, line)  # 匹配结果
                        if res:
                            key = res.group(1)  # 获取按键
                        else:
                            if self.text is not None:
                                self.text.printf("char 键盘正则匹配失败")
                            else:
                                print("char 键盘正则匹配失败")
                    elif "special" in line:
                        mode = re.compile(r"special (.+?) ")  # 正则匹配键盘特殊按键
                        res = re.search(mode, line)  # 匹配结果
                        if res:
                            key = eval(res.group(1))  # 获取按键
                        else:
                            if self.text is not None:
                                self.text.printf("special 键盘正则匹配失败")
                            else:
                                print("special 键盘正则匹配失败")
                    if "pressed" in line:
                        keyboard.press(key)  # 按下按键
                        if self.text is not None:
                            self.text.printf("键盘按下: {0}".format(key))
                        else:
                            print("键盘按下: {0}".format(key))
                    elif "released" in line:
                        keyboard.release(key)  # 释放按键
                        if self.text is not None:
                            self.text.printf("键盘释放: {0}".format(key))
                        else:
                            print("键盘释放: {0}".format(key))
                timestmp = float(line.split(" ")[0])  # 更新操作时间戳
