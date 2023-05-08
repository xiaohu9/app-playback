# APP PLAYBACK ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

本项目是基于Pynput的APP回放工具，用于回放APP的操作过程，并生成操作过程的脚本。\
同时，基于PyQT5插件实现了一个简单的GUI界面，用于操作APP回放工具。

## Installation - 环境配置
    
```bash
pip install -r requirements.txt
```

## Usage - 用法

```bash
python main_win.py
```


## Structure - 项目结构

```
.
│  2023_04_17_13_19_51_Record.txt  // APP回放工具生成的脚本
│  2023_04_17_13_23_09_Record.txt  // APP回放工具生成的脚本
│  list.txt  // 文件结构目录生成
│  main_win.py  // 主程序，用于运行GUI界面和APP回放工具
│  playback.py  // APP回放工具
│  pyqt_gui.py  // GUI界面
│  pyqt_gui.ui  // GUI界面 - QT Designer生成
│  Readme.md  // 说明文档
│  Recorder.py  // APP回放工具
├─ requirements.txt  // 环境配置

```


## Questions - 项目问题

```
没有使用钩子函数来解决鼠标和按键事件的监听，而是使用了Pynput库来监听鼠标和按键事件，这样会导致在录制过程中，如果鼠标移动到了录制窗口之外，或者按下了快捷键，都会导致录制中断。
因此后续需要使用钩子函数来解决这个问题。
```

