import sys
import os
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from pyqt_gui import *
from pynput import mouse, keyboard
from Recorder import Recorder
from playback import Playback


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 初始化表格
        # 设置行数和列数
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 300)
        # 设置表格头部
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("序号"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("文件名"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("修改时间"))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # 获取当前路径下的脚本文件(展示在表格中)
        self.get_scripts()

        # 实例化文本展示框
        self.printf("初始化信息框")

        # 按键事件绑定
        self.pushButton.clicked.connect(self.start_record)
        self.pushButton_2.clicked.connect(self.get_scripts)  # 录制完成后再更新表格中的录制脚本
        self.pushButton_2.clicked.connect(self.stop_record)
        self.pushButton_3.clicked.connect(self.start_playback)
        self.pushButton_4.clicked.connect(self.stop_playback)

        # 建立监听进程
        self.mouse_thread: mouse.Listener = None
        self.keyboard_thread: keyboard.Listener = None
        self.playback_thread: Playback = None

    # 开始录制
    def start_record(self):
        self.setWindowState(Qt.WindowMinimized)  # 开始录制后屏幕最小化
        # 按键在录制时不可点击
        self.pushButton.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.setDisabled(True)
        filename = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(time.time())) + "Record.txt"  # 以当前时间命名文件
        file = os.path.join(os.getcwd(), filename)
        listener = Recorder(file)
        self.mouse_thread = mouse.Listener(on_click=listener.on_click)  # 监听鼠标
        self.keyboard_thread = keyboard.Listener(on_press=listener.on_press, on_release=listener.on_release)  # 监听键盘进程
        self.mouse_thread.start()
        self.keyboard_thread.start()

    # 停止录制
    def stop_record(self):
        if self.mouse_thread is not None:
            if self.mouse_thread.isAlive():
                self.mouse_thread.stop()
        if self.keyboard_thread is not None:
            if self.keyboard_thread.isAlive():
                self.keyboard_thread.stop()
        self.pushButton.setDisabled(False)
        self.pushButton_3.setDisabled(False)
        self.pushButton_4.setDisabled(False)

    # 更新列表中的脚本文件
    def get_scripts(self):
        # 获取当前路径的txt文件
        path = os.getcwd()
        files = []
        for file in os.listdir(path):
            if file.endswith(".txt"):
                files.append(file)
        row_num = len(files)
        self.tableWidget.setRowCount(row_num)
        # 设置数据条目
        for row in range(row_num):
            checked_box = QTableWidgetItem()  # 设置第一列表格内容
            checked_box.setText(str(row + 1))
            checked_box.setCheckState(Qt.Unchecked)  # 设置checkbox为未选中状态
            checked_box.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, 0, checked_box)

            # 设置第二列表格内容
            name = QTableWidgetItem(files[row])
            name.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, 1, name)

            # 设置第三列表格内容
            file_path = os.path.join(path, files[row])
            mtime = os.stat(file_path).st_mtime
            strmtime = time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(mtime))  # 将时间戳转换为时间
            item_time = QTableWidgetItem(strmtime)
            item_time.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, 2, item_time)

    # 获取需要回放的文件列表
    def get_plackbackfiles(self):
        row_num = self.tableWidget.rowCount()
        files = []
        for i in range(row_num):
            if self.tableWidget.item(i, 0).checkState() == Qt.Checked:  # 如果该行被选中
                filename = self.tableWidget.item(i, 1).text()  # 获取文件名
                file = os.path.join(os.getcwd(), filename)  # 获取文件路径
                files.append(file)  # 将文件路径添加到列表中
        return files

    # 开始回放
    def start_playback(self):
        files = self.get_plackbackfiles()
        if len(files) != 0:
            # 按键在回放时不可点击
            self.pushButton.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            self.playback_thread = Playback(files, self)  # 实例化回放线程
            self.playback_thread.start()
            self.playback_thread.finished.connect(self.reset_button)  # 回放结束后恢复按键状态

    def reset_button(self):
        # 按键在回放结束后恢复可点击
        self.pushButton.setDisabled(False)
        self.pushButton_2.setDisabled(False)
        self.pushButton_3.setDisabled(False)
        self.pushButton_4.setDisabled(False)

    # 停止回放
    def stop_playback(self):
        if self.playback_thread is not None:
            if self.playback_thread.isRunning():
                self.playback_thread.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
