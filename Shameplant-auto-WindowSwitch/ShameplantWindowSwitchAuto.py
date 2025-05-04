#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import codecs
import objc
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
import subprocess
import Quartz
try:
    from AppKit import NSWorkspace, NSScreen
    from Foundation import NSObject
except ImportError:
    print("can't import AppKit -- maybe you're running python from homebrew?")
    print("try running with /usr/bin/python instead")
    exit(1)
# from AppKit import NSWorkspace
# from Foundation import NSObject

BasePath = '/Applications/Shameplant.app/Contents/Resources/'  # 资源路径
# BasePath = ''  # 测试

class AppEventListener(NSObject):
    """ 监听 macOS 前台应用变化，避免轮询消耗资源 """

    def init(self):
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

        self = objc.super(AppEventListener, self).init()
        if self is None:
            return None

        nc = NSWorkspace.sharedWorkspace().notificationCenter()
        nc.addObserver_selector_name_object_(
            self, objc.selector(self.app_changed_, signature=b"v@:@"),
            "NSWorkspaceDidActivateApplicationNotification", None
        )
        # nc.addObserver_selector_name_object_(
        #     self, objc.selector(self.app_relaunch, signature=b"v@:@"),
        #     "NSApplicationDidChangeScreenParametersNotification", None  # 监听屏幕变化
        # )
        return self

    def app_changed_(self, sender, notification):
        try:
            # 当前台应用变化时，自动调整 Dock
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
            #pid = self.get_pid_psutil(app_name)

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
            #print(f'{x}, {y}, {width}, {height}')

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

            mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
            mouse_x, mouse_y = int(mouse_location.x), int(mouse_location.y)

            # 获取所有屏幕
            max_displays = 100
            active_displays = Quartz.CGGetActiveDisplayList(max_displays, None, None)[1]

            # 计算鼠标在哪个屏幕
            main_screen = NSScreen.mainScreen()
            frame = main_screen.frame()
            visible_frame = main_screen.visibleFrame()
            self.dock_postion = codecs.open(pos_file, 'r', encoding='utf-8').read()
            for display in active_displays:
                bounds = Quartz.CGDisplayBounds(display)
                x, y, w, h = int(bounds.origin.x), int(bounds.origin.y), int(bounds.size.width), int(bounds.size.height)

                if x <= mouse_x < x + w and y <= mouse_y < y + h:
                    screen_position = f"{display} ({w}x{h})"
                    #print(screen_position)
                    need_re_calculate = codecs.open(BasePath + "Screen2.txt", 'r', encoding='utf-8').read()
                    if need_re_calculate == '1':
                        try:
                            if self.dock_postion == 'x':
                                CMD = '''
                                    on run argv
                                        display notification (item 2 of argv) with title (item 1 of argv)
                                    end run'''
                                self.notify(CMD, "Shameplant: Dynaic Dock",
                                            f"Please go to the Settings panel in the menu bar.")
                            else:
                                with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
                                    f0.write('0')
                                ScriptName = 'Relaunch Shameplant'
                                shortcmd = """set myCommand to "shortcuts run \\"%s\\""
                                    do shell script myCommand""" % ScriptName
                                subprocess.call(['osascript', '-e', shortcmd])
                        except Exception as e:
                            # 发生异常时打印错误信息
                            p = "程序发生异常:" + str(e)
                            with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                                f0.write(p)
                            with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
                                f0.write('1')
                    if need_re_calculate == '0':
                        screen_position_old = codecs.open(BasePath + "Screen.txt", 'r', encoding='utf-8').read()
                        if screen_position_old == '':
                            pass
                        else:
                            if screen_position_old != screen_position:
                                try:
                                    if self.dock_postion == 'x':
                                        CMD = '''
                                            on run argv
                                                display notification (item 2 of argv) with title (item 1 of argv)
                                            end run'''
                                        self.notify(CMD, "Shameplant: Dynaic Dock",
                                                    f"Please go to the Settings panel in the menu bar.")
                                    else:
                                        with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
                                            f0.write('0')
                                        ScriptName = 'Relaunch Shameplant'
                                        shortcmd = """set myCommand to "shortcuts run \\"%s\\""
                                            do shell script myCommand""" % ScriptName
                                        subprocess.call(['osascript', '-e', shortcmd])
                                except Exception as e:
                                    # 发生异常时打印错误信息
                                    p = "程序发生异常:" + str(e)
                                    print(p)
                                    with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                                        f0.write(p)
                                    with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
                                        f0.write('1')
                    with open(BasePath + "Screen.txt", 'w', encoding='utf-8') as f0:
                        f0.write(screen_position)
                    break
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
                f0.write(p)

    # def get_pid_psutil(self, app_name):
    #     for proc in psutil.process_iter(attrs=["pid", "name"]):
    #         try:
    #             if app_name.lower() in proc.info["name"].lower():
    #                 return proc.info["pid"]
    #         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #             continue
    #     return None

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

    # def app_relaunch(self):
    #     sys.exit(0)

    # def restart_program(self):
    #     subprocess.Popen([sys.executable] + sys.argv)
    #     os._exit(0)  # 直接退出当前进程


class window1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 监听事件
        self.listener = AppEventListener.alloc().init()


if __name__ == '__main__':
    while True:
        try:
            app = QApplication(sys.argv)
            app.setQuitOnLastWindowClosed(True)
            w1 = window1()
            app.exec()
        except Exception as e:
            # 发生异常时打印错误信息
            p = "程序发生异常:" + str(e)
            with open(BasePath + "Error.txt", 'w', encoding='utf-8') as f0:
                f0.write(p)
            # 使用 os.execv() 在当前进程中启动自身，实现自动重启
            os.execv(sys.executable, [sys.executable, __file__])

