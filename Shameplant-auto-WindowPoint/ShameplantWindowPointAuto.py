import sys
import os
import time
import codecs
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from pynput import mouse
import Quartz
try:
    from AppKit import NSWorkspace
except ImportError:
    print("can't import AppKit -- maybe you're running python from homebrew?")
    print("try running with /usr/bin/python instead")
    exit(1)

BasePath = '/Applications/Shameplant.app/Contents/Resources/'  # 资源路径
# BasePath = ''  # 测试


class MouseClickListener(QThread):
    click_signal = pyqtSignal(int, int)  # 发送鼠标点击坐标信号
    drag_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.listener = None
        self.start_x = 0
        self.start_y = 0
        self.is_pressed = False
        self.threshold = 3  # 拖拽距离阈值（像素）
        self.last_click_time = 0
        self.click_interval_threshold = 0.25  # 双击节流（秒）

    def run(self):
        with mouse.Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                self.start_x = x
                self.start_y = y
                self.is_pressed = True
            else:
                if not self.is_pressed:
                    return  # 防止状态异常时误触发

                self.is_pressed = False
                distance = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5

                if distance < self.threshold:
                    # 是点击，不是拖拽
                    current_time = time.time()
                    if current_time - self.last_click_time >= self.click_interval_threshold:
                        self.last_click_time = current_time
                        self.click_signal.emit(x, y)
                else:
                    # 是拖拽
                    self.drag_signal.emit(self.start_x, self.start_y)

    def stop(self):
        if self.listener:
            self.listener.stop()
        self.quit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.last_active_name = None
        self.pass_key = 0

        home_dir = str(Path.home())
        tarname1 = "ShameplantAppPath"
        fulldir1 = os.path.join(home_dir, tarname1)
        if not os.path.exists(fulldir1):
            os.mkdir(fulldir1)
        tarname5 = "No.txt"
        self.fulldir5 = os.path.join(fulldir1, tarname5)
        if not os.path.exists(self.fulldir5):
            with open(self.fulldir5, 'a', encoding='utf-8') as f0:
                f0.write('')
        tarname6 = "Always.txt"
        self.fulldir6 = os.path.join(fulldir1, tarname6)
        if not os.path.exists(self.fulldir6):
            with open(self.fulldir6, 'a', encoding='utf-8') as f0:
                f0.write('')
        tarname7 = "Never.txt"
        self.fulldir7 = os.path.join(fulldir1, tarname7)
        if not os.path.exists(self.fulldir7):
            with open(self.fulldir7, 'a', encoding='utf-8') as f0:
                f0.write('')

        # 启动鼠标监听线程
        self.mouse_thread = MouseClickListener()
        self.mouse_thread.click_signal.connect(self.on_click_action)
        self.mouse_thread.start()

    def on_click_action(self, x, y):
        try:
            time.sleep(0.05)
            # self.label.setText(f"拖拽中: ({x}, {y})")
            """ 当前台应用变化时，自动调整 Dock """
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app['NSApplicationName']

            if app_name == "loginwindow":
                return

            never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read()
            never_react_list = never_react.split('\n')
            while '' in never_react_list:
                never_react_list.remove('')

            always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read()
            always_show_list = always_show.split('\n')
            while '' in always_show_list:
                always_show_list.remove('')

            always_hide = codecs.open(self.fulldir7, 'r', encoding='utf-8').read()
            always_hide_list = always_hide.split('\n')
            while '' in always_hide_list:
                always_hide_list.remove('')

            if app_name in never_react_list:
                return

            if app_name in always_show_list:
                toggle_dock_script = 'tell application "System Events" to set the autohide of dock preferences to false'
                os.system(f"osascript -e '{toggle_dock_script}'")
                return

            if app_name in always_hide_list:
                toggle_dock_script = 'tell application "System Events" to set the autohide of dock preferences to true'
                os.system(f"osascript -e '{toggle_dock_script}'")
                return

            if self.last_active_name != None:
                if self.last_active_name != app_name:
                    self.last_active_name = app_name
                    return
                else:
                    self.pass_key = 1
            else:
                self.pass_key = 1

            if self.pass_key == 1:
                # 读取 dock 位置 & 配置参数
                home_dir = str(Path.home())
                settings_dir = os.path.join(home_dir, "ShameplantAppPath")
                pos_file = os.path.join(settings_dir, "Position.txt")
                dist_file = os.path.join(settings_dir, "Distance.txt")
                core_file = os.path.join(BasePath, "core_value.txt")
                basic_file = os.path.join(BasePath, "menu_height.txt")

                if not os.path.exists(pos_file) or not os.path.exists(dist_file) or not os.path.exists(core_file):
                    return

                dock_position = int(codecs.open(pos_file, 'r', encoding='utf-8').read().strip())
                threshold = int(codecs.open(dist_file, 'r', encoding='utf-8').read().strip())
                core_value = int(codecs.open(core_file, 'r', encoding='utf-8').read().strip())
                basic_value = int(codecs.open(basic_file, 'r', encoding='utf-8').read().strip())

                # 获取当前前台应用的应用程序标识符（PID）
                # pid = self.get_pid_psutil(app_name)

                # 使用 Accessibility API 获取该应用的窗口信息
                info = self.get_app_window_info(app_name)
                if info is None:
                    time.sleep(0.5)
                    try:
                        info = self.get_app_window_info(app_name)
                    except Exception as e:
                        # 发生异常时打印错误信息
                        p = "程序发生异常: info is None" + str(e)
                        with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                            f0.write(p)
                x = info[0]
                y = info[1]
                width = info[2]
                height = info[3]

                y_basic_value = 0
                if dock_position == 0:
                    y_basic_value = basic_value - 1
                # 仅对可见窗口做出反应
                if y > y_basic_value and width > 0 and height > 0:
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
                self.last_active_name = app_name
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                f0.write(p)

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
            sys.exit(app.exec())
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'w', encoding='utf-8') as f0:
                f0.write(p)
            # 使用 os.execv() 在当前进程中启动自身，实现自动重启
            os.execv(sys.executable, [sys.executable, __file__])
