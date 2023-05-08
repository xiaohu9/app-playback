import time
from pynput import keyboard
from pynput import mouse


# 用于记录键盘按键事件以及对应间隔
class Recorder:
    def __init__(self, file):
        self.file = file
        self.start_time = time.time()

    # 记录鼠标点击事件
    def on_click(self, x, y, button, pressed):
        # 获取鼠标按键
        if button == mouse.Button.left:
            button_name = 'Left'
        elif button == mouse.Button.middle:
            button_name = 'Middle'
        elif button == mouse.Button.right:
            button_name = 'Right'
        else:
            button_name = 'Unknown'
        if pressed:
            msg = 'Mouse clicked at {0} {1} with {2}'.format(x, y, button_name)
        else:
            msg = 'Mouse released at {0} {1} with {2}'.format(x, y, button_name)
        # 记录鼠标事件
        with open(self.file, 'a') as f:
            f.write(str(time.time() - self.start_time))
            f.write(" ")
            f.write(msg + '\n')

    # 记录键盘按键事件
    def on_press(self, key):
        # 获取按键
        try:
            msg = 'Key char {0} pressed'.format(key.char)
        except AttributeError:
            msg = 'Key special {0} pressed'.format(key)
        # 记录键盘事件
        with open(self.file, 'a') as f:
            f.write(str(time.time() - self.start_time))
            f.write(" ")
            f.write(msg + '\n')

    # 记录键盘释放事件
    def on_release(self, key):
        # 获取按键
        try:
            msg = 'Key char {0} released'.format(key.char)
        except AttributeError:
            msg = 'Key special {0} released'.format(key)
        # 按下esc键退出
        if key == keyboard.Key.esc:
            return False
        # 记录键盘事件
        with open(self.file, 'a') as f:
            f.write(str(time.time() - self.start_time))
            f.write(" ")
            f.write(msg + '\n')
    