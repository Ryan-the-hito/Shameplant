#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import codecs
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from pynput import mouse
import Quartz
import psutil
try:
    from AppKit import NSWorkspace
except ImportError:
    print("can't import AppKit -- maybe you're running python from homebrew?")
    print("try running with /usr/bin/python instead")
    exit(1)

BasePath = '/Applications/Shameplant.app/Contents/Resources/'  # 资源路径
# BasePath = ''  # 测试


class MouseDragListener(QThread):
    drag_signal = pyqtSignal(int, int)  # 发送鼠标拖拽坐标信号

    def __init__(self):
        super().__init__()
        self.listener = None
        self.is_dragging = False
        self.start_x = 0
        self.start_y = 0
        self.threshold = 3  # 拖拽触发阈值（像素）

    def run(self):
        with mouse.Listener(on_click=self.on_click, on_move=self.on_move) as self.listener:
            self.listener.join()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                self.is_dragging = True
                self.start_x = x
                self.start_y = y
            else:
                self.is_dragging = False
                # 计算拖拽距离
                distance = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
                if distance >= self.threshold:
                    self.drag_signal.emit(self.start_x, self.start_y)  # 只有真正拖拽时才触发信号

    def on_move(self, x, y):
        if self.is_dragging:
            pass

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.quit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("PyQt6 + pynput 鼠标拖拽监听")
        # self.setGeometry(100, 100, 400, 200)

        # self.label = QLabel("拖拽时鼠标坐标显示在这里", self)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # self.setLayout(layout)

        # 启动鼠标监听线程
        self.mouse_thread = MouseDragListener()
        self.mouse_thread.drag_signal.connect(self.update_label)
        self.mouse_thread.start()

    def update_label(self, x, y):
        try:
            # self.label.setText(f"拖拽中: ({x}, {y})")
            """ 当前台应用变化时，自动调整 Dock """
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app['NSApplicationName']

            if app_name == "loginwindow":
                return

            # 读取 dock 位置 & 配置参数
            home_dir = str(Path.home())
            settings_dir = os.path.join(home_dir, "ShameplantAppPath")
            pos_file = os.path.join(settings_dir, "Position.txt")
            dist_file = os.path.join(settings_dir, "Distance.txt")
            core_file = os.path.join(BasePath, "core_value.txt")

            if not os.path.exists(pos_file) or not os.path.exists(dist_file) or not os.path.exists(core_file):
                return

            dock_position = int(codecs.open(pos_file, 'r', encoding='utf-8').read().strip())
            threshold = int(codecs.open(dist_file, 'r', encoding='utf-8').read().strip())
            core_value = int(codecs.open(core_file, 'r', encoding='utf-8').read().strip())

            # 获取当前前台应用的应用程序标识符（PID）
            pid = self.get_pid_psutil(app_name)

            # 使用 Accessibility API 获取该应用的窗口信息
            info = self.get_app_window_info(app_name)
            x = info[0]
            y = info[1]
            width = info[2]
            height = info[3]

            compare_value = threshold
            if dock_position == 0:
                compare_value = int(y) + int(height) + threshold
            if dock_position == 1:
                compare_value = int(x) - threshold
            if dock_position == 2:
                compare_value = int(x) + int(width) + threshold

            # 仅在 dock 状态需要变化时执行 AppleScript，减少 CPU 消耗
            if (dock_position == 0 and compare_value >= core_value) or \
                    (dock_position == 1 and compare_value <= core_value) or \
                    (dock_position == 2 and compare_value >= core_value):
                toggle_dock_script = 'tell application "System Events" to set the autohide of dock preferences to true'
            else:
                toggle_dock_script = 'tell application "System Events" to set the autohide of dock preferences to false'

            os.system(f"osascript -e '{toggle_dock_script}'")
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                f0.write(p)

    def get_pid_psutil(self, app_name):
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                if app_name.lower() in proc.info["name"].lower():
                    return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None

    def get_app_window_info(self, app_name):
        # 仅获取当前屏幕上可见的窗口
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
        for window in window_list:
            owner = window.get("kCGWindowOwnerName", "")
            if owner == app_name:
                bounds = window.get("kCGWindowBounds", {})
                x = bounds.get("X", 0)
                y = bounds.get("Y", 0)
                width = bounds.get("Width", 0)
                height = bounds.get("Height", 0)
                return (x, y, width, height)
        return None

    def closeEvent(self, event):
        self.mouse_thread.stop()
        event.accept()

if __name__ == "__main__":
    while True:
        try:
            app = QApplication(sys.argv)
            window = MainWindow()
            #window.show()
            sys.exit(app.exec())
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'w', encoding='utf-8') as f0:
                f0.write(p)
            # 使用 os.execv() 在当前进程中启动自身，实现自动重启
            os.execv(sys.executable, [sys.executable, __file__])

