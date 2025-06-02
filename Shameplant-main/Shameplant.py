#!/usr/local/bin/python3.11
# -*- coding: utf-8 -*-
# -*- encoding:UTF-8 -*-
# coding=utf-8
# coding:utf-8

import codecs
import time

from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
							 QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
							 QSystemTrayIcon, QMenu, QDialog, QMenuBar, QCheckBox, QTextEdit, QComboBox, QListWidget, QFileDialog, QGraphicsOpacityEffect, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QUrl, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QIcon, QColor, QMovie, QDesktopServices, QPixmap
import PyQt6.QtGui
import webbrowser
import sys
import applescript
import subprocess
import signal
from bs4 import BeautifulSoup
import html2text
import urllib3
import logging
import requests
import re
import os
from pathlib import Path
import objc
import shutil
import Quartz
from pynput import mouse
import urllib.parse
import traceback
from functools import partial
try:
	from AppKit import NSWorkspace, NSScreen
	from Foundation import NSObject
except ImportError:
	print("can't import AppKit -- maybe you're running python from homebrew?")
	print("try running with /usr/bin/python instead")
	exit(1)


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

BasePath = '/Applications/Shameplant.app/Contents/Resources/'
#BasePath = ''  # test

# Create the icon
icon = QIcon(BasePath + "Shameplant_menu.icns")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()

action3 = QAction("🌾 Switch on Shameplant!")
action3.setCheckable(True)
menu.addAction(action3)

settings_menu = QMenu("🏹 Set rule for the topmost app")
menu.addMenu(settings_menu)
# 保留 action 引用，防止被回收（可选但推荐）
action_refs = []
# updade
def on_config_clicked(config_name):
	#print(f"Clicked: {config_name}")
	home_dir = str(Path.home())
	tarname1 = "ShameplantAppPath"
	fulldir1 = os.path.join(home_dir, tarname1)
	if not os.path.exists(fulldir1):
		os.mkdir(fulldir1)
	tarname5 = "No.txt"
	fulldir5 = os.path.join(fulldir1, tarname5)
	if not os.path.exists(fulldir5):
		with open(fulldir5, 'a', encoding='utf-8') as f0:
			f0.write('')
	tarname6 = "Always.txt"
	fulldir6 = os.path.join(fulldir1, tarname6)
	if not os.path.exists(fulldir6):
		with open(fulldir6, 'a', encoding='utf-8') as f0:
			f0.write('')
	tarname7 = "Never.txt"
	fulldir7 = os.path.join(fulldir1, tarname7)
	if not os.path.exists(fulldir7):
		with open(fulldir7, 'a', encoding='utf-8') as f0:
			f0.write('')

	active_app = NSWorkspace.sharedWorkspace().activeApplication()
	app_name = active_app['NSApplicationName']

	if config_name != "Never react" and config_name != "Always show" and config_name != 'Always hide':
		settings_menu.clear()
		for name in [f"🔝{app_name}", "Never react", "Always show", 'Always hide']:
			action = QAction(name, settings_menu)
			action.triggered.connect(partial(on_config_clicked, name))
			settings_menu.addAction(action)
			action_refs.append(action)  # 避免垃圾回收
	if config_name == "Never react":
		never_react = codecs.open(fulldir5, 'r', encoding='utf-8').read()
		never_react_list = never_react.split('\n')
		while '' in never_react_list:
			never_react_list.remove('')
		if app_name not in never_react_list:
			with open(fulldir5, 'a', encoding='utf-8') as f0:
				f0.write(app_name + '\n')
			never_react = codecs.open(fulldir5, 'r', encoding='utf-8').read().lstrip('\n')
			with open(fulldir5, 'w', encoding='utf-8') as f0:
				f0.write(never_react)
	if config_name == "Always show":
		never_react = codecs.open(fulldir6, 'r', encoding='utf-8').read()
		never_react_list = never_react.split('\n')
		while '' in never_react_list:
			never_react_list.remove('')
		if app_name not in never_react_list:
			with open(fulldir6, 'a', encoding='utf-8') as f0:
				f0.write(app_name + '\n')
			never_react = codecs.open(fulldir6, 'r', encoding='utf-8').read().lstrip('\n')
			with open(fulldir6, 'w', encoding='utf-8') as f0:
				f0.write(never_react)
	if config_name == "Always hide":
		never_react = codecs.open(fulldir7, 'r', encoding='utf-8').read()
		never_react_list = never_react.split('\n')
		while '' in never_react_list:
			never_react_list.remove('')
		if app_name not in never_react_list:
			with open(fulldir7, 'a', encoding='utf-8') as f0:
				f0.write(app_name + '\n')
			never_react = codecs.open(fulldir7, 'r', encoding='utf-8').read().lstrip('\n')
			with open(fulldir7, 'w', encoding='utf-8') as f0:
				f0.write(never_react)
# 添加多个菜单项并绑定函数
active_app = NSWorkspace.sharedWorkspace().activeApplication()
app_name = active_app['NSApplicationName']
for name in [f"🔝{app_name}", "Never react", "Always show", 'Always hide']:
	action = QAction(name, settings_menu)
	action.triggered.connect(partial(on_config_clicked, name))
	settings_menu.addAction(action)
	action_refs.append(action)  # 避免垃圾回收

def on_tray_icon_clicked():
	settings_menu.clear()
	active_app = NSWorkspace.sharedWorkspace().activeApplication()
	app_name = active_app['NSApplicationName']
	for name in [f"🔝{app_name}", "Never react", "Always show", 'Always hide']:
		action = QAction(name, settings_menu)
		action.triggered.connect(partial(on_config_clicked, name))
		settings_menu.addAction(action)
		action_refs.append(action)  # 避免垃圾回收
tray.activated.connect(on_tray_icon_clicked)

menu.addSeparator()

action7 = QAction("⚙️ Settings")
menu.addAction(action7)

action10 = QAction("🛠️ Start on login")
action10.setCheckable(True)
menu.addAction(action10)

menu.addSeparator()

action2 = QAction("🆕 Check for Updates")
menu.addAction(action2)

action1 = QAction("ℹ️ About")
menu.addAction(action1)

action9 = QAction("🔤 Guide and Support")
menu.addAction(action9)

menu.addSeparator()

action8 = QAction("🔁 Restart")
menu.addAction(action8)

# Add a Quit option to the menu.
quit = QAction("Quit")
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

# create a system menu
btna4 = QAction("&Switch on Shameplant!")
btna5 = QAction("&Set!")
btna6 = QAction("&Quit!")
sysmenu = QMenuBar()
file_menu = sysmenu.addMenu("&Actions")
file_menu.addAction(btna4)
file_menu.addAction(btna5)
file_menu.addAction(btna6)


class window_about(QWidget):  # 增加说明页面(About)
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):  # 说明页面内信息
		self.setUpMainWindow()
		self.resize(400, 410)
		self.center()
		self.setWindowTitle('About')
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def setUpMainWindow(self):
		widg1 = QWidget()
		l1 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'Shameplant_menu.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l1.setMaximumWidth(100)
		l1.setMaximumHeight(100)
		l1.setScaledContents(True)
		blay1 = QHBoxLayout()
		blay1.setContentsMargins(0, 0, 0, 0)
		blay1.addStretch()
		blay1.addWidget(l1)
		blay1.addStretch()
		widg1.setLayout(blay1)

		widg2 = QWidget()
		lbl0 = QLabel('Shameplant', self)
		font = PyQt6.QtGui.QFont()
		font.setFamily("Arial")
		font.setBold(True)
		font.setPointSize(20)
		lbl0.setFont(font)
		blay2 = QHBoxLayout()
		blay2.setContentsMargins(0, 0, 0, 0)
		blay2.addStretch()
		blay2.addWidget(lbl0)
		blay2.addStretch()
		widg2.setLayout(blay2)

		widg3 = QWidget()
		lbl1 = QLabel('Version 1.0.3', self)
		blay3 = QHBoxLayout()
		blay3.setContentsMargins(0, 0, 0, 0)
		blay3.addStretch()
		blay3.addWidget(lbl1)
		blay3.addStretch()
		widg3.setLayout(blay3)

		widg4 = QWidget()
		lbl2 = QLabel('Thanks for your love🤟.', self)
		blay4 = QHBoxLayout()
		blay4.setContentsMargins(0, 0, 0, 0)
		blay4.addStretch()
		blay4.addWidget(lbl2)
		blay4.addStretch()
		widg4.setLayout(blay4)

		widg5 = QWidget()
		lbl3 = QLabel('感谢您的喜爱！', self)
		blay5 = QHBoxLayout()
		blay5.setContentsMargins(0, 0, 0, 0)
		blay5.addStretch()
		blay5.addWidget(lbl3)
		blay5.addStretch()
		widg5.setLayout(blay5)

		widg6 = QWidget()
		lbl4 = QLabel('♥‿♥', self)
		blay6 = QHBoxLayout()
		blay6.setContentsMargins(0, 0, 0, 0)
		blay6.addStretch()
		blay6.addWidget(lbl4)
		blay6.addStretch()
		widg6.setLayout(blay6)

		widg7 = QWidget()
		lbl5 = QLabel('※\(^o^)/※', self)
		blay7 = QHBoxLayout()
		blay7.setContentsMargins(0, 0, 0, 0)
		blay7.addStretch()
		blay7.addWidget(lbl5)
		blay7.addStretch()
		widg7.setLayout(blay7)

		widg8 = QWidget()
		bt1 = QPushButton('The Author', self)
		bt1.setMaximumHeight(20)
		bt1.setMinimumWidth(100)
		bt1.clicked.connect(self.intro)
		bt2 = QPushButton('Github Page', self)
		bt2.setMaximumHeight(20)
		bt2.setMinimumWidth(100)
		bt2.clicked.connect(self.homepage)
		blay8 = QHBoxLayout()
		blay8.setContentsMargins(0, 0, 0, 0)
		blay8.addStretch()
		blay8.addWidget(bt1)
		blay8.addWidget(bt2)
		blay8.addStretch()
		widg8.setLayout(blay8)

		bt7 = QPushButton('Buy me a cup of coffee☕', self)
		bt7.setMaximumHeight(20)
		bt7.setMinimumWidth(215)
		bt7.clicked.connect(self.coffee)

		widg8_5 = QWidget()
		blay8_5 = QHBoxLayout()
		blay8_5.setContentsMargins(0, 0, 0, 0)
		blay8_5.addStretch()
		blay8_5.addWidget(bt7)
		blay8_5.addStretch()
		widg8_5.setLayout(blay8_5)

		widg9 = QWidget()
		bt3 = QPushButton('🍪\n¥5', self)
		bt3.setMaximumHeight(50)
		bt3.setMinimumHeight(50)
		bt3.setMinimumWidth(50)
		bt3.clicked.connect(self.donate)
		bt4 = QPushButton('🥪\n¥10', self)
		bt4.setMaximumHeight(50)
		bt4.setMinimumHeight(50)
		bt4.setMinimumWidth(50)
		bt4.clicked.connect(self.donate2)
		bt5 = QPushButton('🍜\n¥20', self)
		bt5.setMaximumHeight(50)
		bt5.setMinimumHeight(50)
		bt5.setMinimumWidth(50)
		bt5.clicked.connect(self.donate3)
		bt6 = QPushButton('🍕\n¥50', self)
		bt6.setMaximumHeight(50)
		bt6.setMinimumHeight(50)
		bt6.setMinimumWidth(50)
		bt6.clicked.connect(self.donate4)
		blay9 = QHBoxLayout()
		blay9.setContentsMargins(0, 0, 0, 0)
		blay9.addStretch()
		blay9.addWidget(bt3)
		blay9.addWidget(bt4)
		blay9.addWidget(bt5)
		blay9.addWidget(bt6)
		blay9.addStretch()
		widg9.setLayout(blay9)

		widg10 = QWidget()
		lbl6 = QLabel('© 2022-2025 Ryan-the-hito. All rights reserved.', self)
		blay10 = QHBoxLayout()
		blay10.setContentsMargins(0, 0, 0, 0)
		blay10.addStretch()
		blay10.addWidget(lbl6)
		blay10.addStretch()
		widg10.setLayout(blay10)

		main_h_box = QVBoxLayout()
		main_h_box.addWidget(widg1)
		main_h_box.addWidget(widg2)
		main_h_box.addWidget(widg3)
		main_h_box.addWidget(widg4)
		main_h_box.addWidget(widg5)
		main_h_box.addWidget(widg6)
		main_h_box.addWidget(widg7)
		main_h_box.addWidget(widg8)
		main_h_box.addWidget(widg8_5)
		main_h_box.addWidget(widg9)
		main_h_box.addWidget(widg10)
		main_h_box.addStretch()
		self.setLayout(main_h_box)

	def intro(self):
		webbrowser.open('https://github.com/Ryan-the-hito/Ryan-the-hito')

	def homepage(self):
		webbrowser.open('https://github.com/Ryan-the-hito/Shameplant')

	def coffee(self):
		webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

	def donate(self):
		dlg = CustomDialog()
		dlg.exec()

	def donate2(self):
		dlg = CustomDialog2()
		dlg.exec()

	def donate3(self):
		dlg = CustomDialog3()
		dlg.exec()

	def donate4(self):
		dlg = CustomDialog4()
		dlg.exec()

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def activate(self):  # 设置窗口显示
		self.show()


class CustomDialog(QDialog):  # (About1)
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setUpMainWindow()
		self.setWindowTitle("Thank you for your support!")
		self.center()
		self.resize(400, 390)
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def setUpMainWindow(self):
		widge_all = QWidget()
		l1 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'wechat5.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l1.setMaximumSize(160, 240)
		l1.setScaledContents(True)
		l2 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'alipay5.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l2.setMaximumSize(160, 240)
		l2.setScaledContents(True)
		bk = QHBoxLayout()
		bk.setContentsMargins(0, 0, 0, 0)
		bk.addWidget(l1)
		bk.addWidget(l2)
		widge_all.setLayout(bk)

		m1 = QLabel('Thank you for your kind support! 😊', self)
		m2 = QLabel('I will write more interesting apps! 🥳', self)

		widg_c = QWidget()
		bt1 = QPushButton('Thank you!', self)
		bt1.setMaximumHeight(20)
		bt1.setMinimumWidth(100)
		bt1.clicked.connect(self.cancel)
		bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
		bt2.setMaximumHeight(20)
		bt2.setMinimumWidth(260)
		bt2.clicked.connect(self.coffee)
		blay8 = QHBoxLayout()
		blay8.setContentsMargins(0, 0, 0, 0)
		blay8.addStretch()
		blay8.addWidget(bt1)
		blay8.addWidget(bt2)
		blay8.addStretch()
		widg_c.setLayout(blay8)

		self.layout = QVBoxLayout()
		self.layout.addWidget(widge_all)
		self.layout.addWidget(m1)
		self.layout.addWidget(m2)
		self.layout.addStretch()
		self.layout.addWidget(widg_c)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def coffee(self):
		webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

	def cancel(self):  # 设置取消键的功能
		self.close()


class CustomDialog2(QDialog):  # (About2)
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setUpMainWindow()
		self.setWindowTitle("Thank you for your support!")
		self.center()
		self.resize(400, 390)
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def setUpMainWindow(self):
		widge_all = QWidget()
		l1 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'wechat10.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l1.setMaximumSize(160, 240)
		l1.setScaledContents(True)
		l2 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'alipay10.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l2.setMaximumSize(160, 240)
		l2.setScaledContents(True)
		bk = QHBoxLayout()
		bk.setContentsMargins(0, 0, 0, 0)
		bk.addWidget(l1)
		bk.addWidget(l2)
		widge_all.setLayout(bk)

		m1 = QLabel('Thank you for your kind support! 😊', self)
		m2 = QLabel('I will write more interesting apps! 🥳', self)

		widg_c = QWidget()
		bt1 = QPushButton('Thank you!', self)
		bt1.setMaximumHeight(20)
		bt1.setMinimumWidth(100)
		bt1.clicked.connect(self.cancel)
		bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
		bt2.setMaximumHeight(20)
		bt2.setMinimumWidth(260)
		bt2.clicked.connect(self.coffee)
		blay8 = QHBoxLayout()
		blay8.setContentsMargins(0, 0, 0, 0)
		blay8.addStretch()
		blay8.addWidget(bt1)
		blay8.addWidget(bt2)
		blay8.addStretch()
		widg_c.setLayout(blay8)

		self.layout = QVBoxLayout()
		self.layout.addWidget(widge_all)
		self.layout.addWidget(m1)
		self.layout.addWidget(m2)
		self.layout.addStretch()
		self.layout.addWidget(widg_c)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def coffee(self):
		webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

	def cancel(self):  # 设置取消键的功能
		self.close()


class CustomDialog3(QDialog):  # (About3)
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setUpMainWindow()
		self.setWindowTitle("Thank you for your support!")
		self.center()
		self.resize(400, 390)
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def setUpMainWindow(self):
		widge_all = QWidget()
		l1 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'wechat20.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l1.setMaximumSize(160, 240)
		l1.setScaledContents(True)
		l2 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'alipay20.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l2.setMaximumSize(160, 240)
		l2.setScaledContents(True)
		bk = QHBoxLayout()
		bk.setContentsMargins(0, 0, 0, 0)
		bk.addWidget(l1)
		bk.addWidget(l2)
		widge_all.setLayout(bk)

		m1 = QLabel('Thank you for your kind support! 😊', self)
		m2 = QLabel('I will write more interesting apps! 🥳', self)

		widg_c = QWidget()
		bt1 = QPushButton('Thank you!', self)
		bt1.setMaximumHeight(20)
		bt1.setMinimumWidth(100)
		bt1.clicked.connect(self.cancel)
		bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
		bt2.setMaximumHeight(20)
		bt2.setMinimumWidth(260)
		bt2.clicked.connect(self.coffee)
		blay8 = QHBoxLayout()
		blay8.setContentsMargins(0, 0, 0, 0)
		blay8.addStretch()
		blay8.addWidget(bt1)
		blay8.addWidget(bt2)
		blay8.addStretch()
		widg_c.setLayout(blay8)

		self.layout = QVBoxLayout()
		self.layout.addWidget(widge_all)
		self.layout.addWidget(m1)
		self.layout.addWidget(m2)
		self.layout.addStretch()
		self.layout.addWidget(widg_c)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def coffee(self):
		webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

	def cancel(self):  # 设置取消键的功能
		self.close()


class CustomDialog4(QDialog):  # (About4)
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setUpMainWindow()
		self.setWindowTitle("Thank you for your support!")
		self.center()
		self.resize(400, 390)
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def setUpMainWindow(self):
		widge_all = QWidget()
		l1 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'wechat50.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l1.setPixmap(png)  # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l1.setMaximumSize(160, 240)
		l1.setScaledContents(True)
		l2 = QLabel(self)
		png = PyQt6.QtGui.QPixmap(BasePath + 'alipay50.png')  # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
		l2.setPixmap(png)  # 在l2里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
		l2.setMaximumSize(160, 240)
		l2.setScaledContents(True)
		bk = QHBoxLayout()
		bk.setContentsMargins(0, 0, 0, 0)
		bk.addWidget(l1)
		bk.addWidget(l2)
		widge_all.setLayout(bk)

		m1 = QLabel('Thank you for your kind support! 😊', self)
		m2 = QLabel('I will write more interesting apps! 🥳', self)

		widg_c = QWidget()
		bt1 = QPushButton('Thank you!', self)
		bt1.setMaximumHeight(20)
		bt1.setMinimumWidth(100)
		bt1.clicked.connect(self.cancel)
		bt2 = QPushButton('Neither one above? Buy me a coffee~', self)
		bt2.setMaximumHeight(20)
		bt2.setMinimumWidth(260)
		bt2.clicked.connect(self.coffee)
		blay8 = QHBoxLayout()
		blay8.setContentsMargins(0, 0, 0, 0)
		blay8.addStretch()
		blay8.addWidget(bt1)
		blay8.addWidget(bt2)
		blay8.addStretch()
		widg_c.setLayout(blay8)

		self.layout = QVBoxLayout()
		self.layout.addWidget(widge_all)
		self.layout.addWidget(m1)
		self.layout.addWidget(m2)
		self.layout.addStretch()
		self.layout.addWidget(widg_c)
		self.layout.addStretch()
		self.setLayout(self.layout)

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def coffee(self):
		webbrowser.open('https://www.buymeacoffee.com/ryanthehito')

	def cancel(self):  # 设置取消键的功能
		self.close()


class window_update(QWidget):  # 增加更新页面（Check for Updates）
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):  # 说明页面内信息

		self.lbl = QLabel('Current Version: v1.0.3', self)
		self.lbl.move(30, 45)

		lbl0 = QLabel('Download Update:', self)
		lbl0.move(30, 75)

		lbl1 = QLabel('Latest Version:', self)
		lbl1.move(30, 15)

		self.lbl2 = QLabel('', self)
		self.lbl2.move(122, 15)

		bt1 = QPushButton('Github', self)
		bt1.setFixedWidth(120)
		bt1.clicked.connect(self.upd)
		bt1.move(150, 75)

		bt2 = QPushButton('Baidu Net Disk', self)
		bt2.setFixedWidth(120)
		bt2.clicked.connect(self.upd2)
		bt2.move(150, 105)

		self.resize(300, 150)
		self.center()
		self.setWindowTitle('Shameplant Updates')
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

	def upd(self):
		webbrowser.open('https://github.com/Ryan-the-hito/Shameplant/releases')

	def upd2(self):
		webbrowser.open('https://pan.baidu.com/s/1qiqqRuW8yURvOyemDou1Jg?pwd=dqkg')

	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def activate(self):  # 设置窗口显示
		self.show()
		self.checkupdate()

	def checkupdate(self):
		targetURL = 'https://github.com/Ryan-the-hito/Shameplant/releases'
		try:
			# Fetch the HTML content from the URL
			urllib3.disable_warnings()
			logging.captureWarnings(True)
			s = requests.session()
			s.keep_alive = False  # 关闭多余连接
			response = s.get(targetURL, verify=False)
			response.encoding = 'utf-8'
			html_content = response.text
			# Parse the HTML using BeautifulSoup
			soup = BeautifulSoup(html_content, "html.parser")
			# Remove all images from the parsed HTML
			for img in soup.find_all("img"):
				img.decompose()
			# Convert the parsed HTML to plain text using html2text
			text_maker = html2text.HTML2Text()
			text_maker.ignore_links = True
			text_maker.ignore_images = True
			plain_text = text_maker.handle(str(soup))
			# Convert the plain text to UTF-8
			plain_text_utf8 = plain_text.encode(response.encoding).decode("utf-8")

			for i in range(10):
				plain_text_utf8 = plain_text_utf8.replace('\n\n\n\n', '\n\n')
				plain_text_utf8 = plain_text_utf8.replace('\n\n\n', '\n\n')
				plain_text_utf8 = plain_text_utf8.replace('   ', ' ')
				plain_text_utf8 = plain_text_utf8.replace('  ', ' ')

			pattern2 = re.compile(r'(v\d+\.\d+\.\d+)\sLatest')
			result = pattern2.findall(plain_text_utf8)
			result = ''.join(result)
			nowversion = self.lbl.text().replace('Current Version: ', '')
			if result == nowversion:
				alertupdate = result + '. You are up to date!'
				self.lbl2.setText(alertupdate)
				self.lbl2.adjustSize()
			else:
				alertupdate = result + ' is ready!'
				self.lbl2.setText(alertupdate)
				self.lbl2.adjustSize()
		except:
			alertupdate = 'No Intrenet'
			self.lbl2.setText(alertupdate)
			self.lbl2.adjustSize()


class Slide(QWidget): # guide page
	def __init__(self, text, color, image_path=None, gif_path=None, acc_button=False, font=24, show_button=False, acc_button2=False):
		super().__init__()
		self.setStyleSheet(f"background-color: {color};border-radius:4px;")
		w3 = QWidget()
		layout = QVBoxLayout()
		layout.setSpacing(20)  # 设置控件间距为 0
		layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为 0

		# 图片部分
		if image_path:
			self.image_label = QLabel()
			pixmap = QPixmap(image_path).scaledToHeight(300)
			self.image_label.setPixmap(pixmap)
			self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			layout.addWidget(self.image_label)

		# Gif part
		if gif_path:
			self.gif_label = QLabel()
			#self.gif_label.setFixedWidth(250)
			movie = QMovie(gif_path)
			movie.setScaledSize(QSize(922, 264))
			self.gif_label.setMovie(movie)
			#movie.setSpeed(50)
			movie.start()  # 一定要启动！
			self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			layout.addWidget(self.gif_label)
			# 设置定时器：3 秒后隐藏图片
			QTimer.singleShot(5200, self.hide_image)

		# 按钮（仅当 show_button=True 时）
		if show_button:
			button_layout = QHBoxLayout()

			button_layout.addStretch()

			btn1 = QPushButton("Documentation📑")
			btn1.setFixedWidth(200)
			btn1.clicked.connect(self.handle_feature_a)
			button_layout.addWidget(btn1)
			btn1.setStyleSheet('''
				QPushButton{
				border: 1px outset grey;
				background-color: #FFFFFF;
				border-radius: 4px;
				padding: 1px;
				color: #000000
			}
				QPushButton:pressed{
					border: 1px outset grey;
					background-color: #0085FF;
					border-radius: 4px;
					padding: 1px;
					color: #FFFFFF
			}''')

			button_layout.addStretch()

			btn2 = QPushButton("Tip me!❤️")
			btn2.setFixedWidth(200)
			btn2.clicked.connect(self.handle_feature_b)
			button_layout.addWidget(btn2)
			btn2.setStyleSheet('''
				QPushButton{
				border: 1px outset grey;
				background-color: #FFFFFF;
				border-radius: 4px;
				padding: 1px;
				color: #000000
			}
				QPushButton:pressed{
					border: 1px outset grey;
					background-color: #0085FF;
					border-radius: 4px;
					padding: 1px;
					color: #FFFFFF
			}''')

			button_layout.addStretch()

			btn3 = QPushButton("Bugs? Email me💌")
			btn3.setFixedWidth(200)
			btn3.clicked.connect(self.handle_feature_c)
			button_layout.addWidget(btn3)
			btn3.setStyleSheet('''
				QPushButton{
				border: 1px outset grey;
				background-color: #FFFFFF;
				border-radius: 4px;
				padding: 1px;
				color: #000000
			}
				QPushButton:pressed{
					border: 1px outset grey;
					background-color: #0085FF;
					border-radius: 4px;
					padding: 1px;
					color: #FFFFFF
			}''')

			button_layout.addStretch()

			layout.addLayout(button_layout)

		# 按钮（仅当 acc_button=True 时）
		if acc_button:
			btn4 = QPushButton("Open Accessibility")
			btn4.setFixedWidth(200)
			btn4.clicked.connect(self.handle_feature_d)
			btn4.setStyleSheet('''
				QPushButton{
				border: 1px outset grey;
				background-color: #FFFFFF;
				border-radius: 4px;
				padding: 1px;
				color: #000000
			}
				QPushButton:pressed{
					border: 1px outset grey;
					background-color: #0085FF;
					border-radius: 4px;
					padding: 1px;
					color: #FFFFFF
			}''')
			acc_layout = QHBoxLayout()
			acc_layout.setContentsMargins(0, 0, 0, 0)
			acc_layout.addStretch()
			acc_layout.addWidget(btn4)
			acc_layout.addStretch()
			layout.addLayout(acc_layout)

		# acc2
		if acc_button2:
			btn5 = QPushButton("Open Input Monitoring")
			btn5.setFixedWidth(200)
			btn5.clicked.connect(self.handle_feature_e)
			btn5.setStyleSheet('''
				QPushButton{
				border: 1px outset grey;
				background-color: #FFFFFF;
				border-radius: 4px;
				padding: 1px;
				color: #000000
			}
				QPushButton:pressed{
					border: 1px outset grey;
					background-color: #0085FF;
					border-radius: 4px;
					padding: 1px;
					color: #FFFFFF
			}''')
			acc_layout2 = QHBoxLayout()
			acc_layout2.setContentsMargins(0, 0, 0, 0)
			acc_layout2.addStretch()
			acc_layout2.addWidget(btn5)
			acc_layout2.addStretch()
			layout.addLayout(acc_layout2)

		# 文字部分
		self.label = QLabel(text)
		self.label.setStyleSheet(f"font-size: {font}px; color: black; font: bold Helvetica;")
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		if gif_path:
			self.label.setVisible(False)

			# 添加不透明度效果
			self.opacity_effect = QGraphicsOpacityEffect()
			self.label.setGraphicsEffect(self.opacity_effect)
			self.opacity_effect.setOpacity(0)  # 初始为完全透明

			# 创建动画
			self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
			self.animation.setDuration(2000)  # 动画时长：2000 毫秒
			self.animation.setStartValue(0)
			self.animation.setEndValue(1)
			self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

		#layout.addStretch()
		layout.addWidget(self.label)

		w3.setLayout(layout)
		w3.setStyleSheet('''
			border: 1px solid white;
			background: white;
			border-radius: 9px;
		''')

		blayend = QHBoxLayout()
		blayend.setContentsMargins(0, 0, 0, 0)
		blayend.addWidget(w3)
		self.setLayout(blayend)

	def hide_image(self):
		if self.gif_label:
			self.gif_label.hide()
			self.label.setVisible(True)# 或者 self.image_label.deleteLater() 完全移除
			self.animation.start()

	def handle_feature_a(self):
		webbrowser.open('https://github.com/Ryan-the-hito/Shameplant')

	def handle_feature_b(self):
		w1.show()


	def handle_feature_c(self):
		to = "sweeter.02.implant@icloud.com"
		subject = "[Feedback-Shameplant]"
		body = "\n\n---\nShameplant v1.0.3"
		# 对 subject 和 body 进行 URL 编码
		subject_encoded = urllib.parse.quote(subject)
		body_encoded = urllib.parse.quote(body)

		# 构造 mailto 链接
		mailto_link = f"mailto:{to}?subject={subject_encoded}&body={body_encoded}"

		# 打开默认邮件客户端
		QDesktopServices.openUrl(QUrl(mailto_link))

	def handle_feature_d(self):
		QDesktopServices.openUrl(QUrl("x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"))

	def handle_feature_e(self):
		toggle_dock_script = '''
			tell application "System Settings"
				quit
			end tell
			delay 1
			tell application "System Settings"
				activate
			end tell
			delay 1
			tell application "System Events"
				tell process "System Settings"
					click menu item "Privacy & Security" of menu "View" of menu bar 1
					delay 1
					click button 8 of group 4 of scroll area 1 of group 1 of group 2 of splitter group 1 of group 1 of window "Privacy & Security" of application process "System Settings" of application "System Events"
				end tell
			end tell
		'''
		# 运行AppleScript
		subprocess.run(["osascript", "-e", toggle_dock_script])


class SliderWindow(QWidget): # inside pages of guidance
	def __init__(self):
		super().__init__()
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
		self.resize(960, 550)

		self.stack = QStackedWidget()
		gifpath = BasePath + 'dock9.gif'
		imagepath1 = BasePath + 'access1.png'
		imagepath2 = BasePath + 'access2.png'
		imagepath3 = BasePath + 'access3.png'
		imagepath4 = BasePath + 'promote.png'
		self.slides = [
			Slide("Welcome to Shameplant!", "white", None, f'{gifpath}', False, 50),
			Slide("Allow automation", "white", f'{imagepath1}', None, False),
			Slide("Set up Accessibility", "white", f'{imagepath2}', None, True),
			Slide("Set up Input Monitoring", "white", f'{imagepath3}', None, False, 24, False, True),
			Slide("For more apps and info...", "white", f'{imagepath4}', None, False, 24, True),
			Slide("Thank you for using Shameplant! \n Let's get started!", "white", None, None, False, 45),
		]

		for slide in self.slides:
			self.stack.addWidget(slide)

		# 页码圆点
		self.dots = [QLabel("●") for _ in self.slides]
		for dot in self.dots:
			dot.setStyleSheet("font-size: 16px; color: lightgray;")
		self.update_dots(0)

		dots_layout = QHBoxLayout()
		dots_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		for dot in self.dots:
			dots_layout.addWidget(dot)

		# 翻页按钮
		self.prev_btn = QPushButton("←")
		self.prev_btn.setFixedWidth(100)
		self.next_btn = QPushButton("→")
		self.next_btn.setFixedWidth(100)
		self.prev_btn.clicked.connect(self.go_prev)
		self.next_btn.clicked.connect(self.go_next)
		self.prev_btn.setStyleSheet('''
			QPushButton{
			border: 1px outset grey;
			background-color: #FFFFFF;
			border-radius: 4px;
			padding: 1px;
			color: #000000
		}
			QPushButton:pressed{
				border: 1px outset grey;
				background-color: #0085FF;
				border-radius: 4px;
				padding: 1px;
				color: #FFFFFF
		}''')
		self.next_btn.setStyleSheet('''
			QPushButton{
			border: 1px outset grey;
			background-color: #FFFFFF;
			border-radius: 4px;
			padding: 1px;
			color: #000000
		}
			QPushButton:pressed{
				border: 1px outset grey;
				background-color: #0085FF;
				border-radius: 4px;
				padding: 1px;
				color: #FFFFFF
		}''')

		btn_layout = QHBoxLayout()
		btn_layout.addStretch()
		btn_layout.addWidget(self.prev_btn)
		btn_layout.addStretch()
		btn_layout.addWidget(self.next_btn)
		btn_layout.addStretch()

		w3 = QWidget()
		blay3 = QVBoxLayout()
		blay3.setContentsMargins(0, 0, 0, 0)
		blay3.addStretch()
		blay3.addWidget(self.stack)
		blay3.addLayout(dots_layout)
		blay3.addLayout(btn_layout)
		blay3.addStretch()
		w3.setLayout(blay3)
		w3.setStyleSheet('''
			border: 1px solid white;
			background: white;
			border-radius: 9px;
		''')

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(w3)
		self.setLayout(layout)

		self.current_index = 0

	def update_dots(self, index):
		for i, dot in enumerate(self.dots):
			color = "black" if i == index else "lightgray"
			dot.setStyleSheet(f"font-size: 16px; color: {color};")

	def slide_to(self, new_index):
		if new_index < 0 or new_index >= self.stack.count():
			home_dir = str(Path.home())
			tarname1 = "ShameplantAppPath"
			fulldir1 = os.path.join(home_dir, tarname1)
			if not os.path.exists(fulldir1):
				os.mkdir(fulldir1)
			tarname8 = "New.txt"
			self.fulldir8 = os.path.join(fulldir1, tarname8)
			if not os.path.exists(self.fulldir8):
				with open(self.fulldir8, 'a', encoding='utf-8') as f0:
					f0.write('0')
			with open(self.fulldir8, 'w', encoding='utf-8') as f0:
				f0.write('1')
			self.close()
		else:
			current_widget = self.stack.currentWidget()
			next_widget = self.stack.widget(new_index)

			direction = -1 if new_index > self.current_index else 1
			offset = self.stack.width() * direction

			next_widget.setGeometry(self.stack.geometry().translated(offset, 0))
			next_widget.show()

			anim_current = QPropertyAnimation(current_widget, b"geometry")
			anim_next = QPropertyAnimation(next_widget, b"geometry")

			rect = self.stack.geometry()

			anim_current.setDuration(300)
			anim_current.setStartValue(rect)
			anim_current.setEndValue(rect.translated(-offset, 0))

			anim_next.setDuration(300)
			anim_next.setStartValue(rect.translated(offset, 0))
			anim_next.setEndValue(rect)

			anim_current.setEasingCurve(QEasingCurve.Type.OutCubic)
			anim_next.setEasingCurve(QEasingCurve.Type.OutCubic)

			anim_current.start()
			anim_next.start()

			self.stack.setCurrentIndex(new_index)
			self.current_index = new_index
			self.update_dots(new_index)

	def go_next(self):
		self.slide_to(self.current_index + 1)

	def go_prev(self):
		self.slide_to(self.current_index - 1)


class TimerThread(QThread):
	tick = pyqtSignal()  # 用于向主线程发信号

	def run(self):
		# 在子线程中创建一个定时器
		self.timer = QTimer()
		self.timer.setInterval(60 * 1000)  # 60秒
		self.timer.timeout.connect(self.on_timeout)
		self.timer.start()

		# 启动事件循环，这很重要！
		self.exec()

	def on_timeout(self):
		self.tick.emit()  # 发出信号通知主线程

	def stop(self):
		if hasattr(self, 'timer') and self.timer.isActive():
			self.timer.stop()
		self.quit()  # 结束事件循环
		self.wait()  # 等待线程安全退出


class AppEventListener(NSObject): # WindowSwitchAuto
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
		#	 self, objc.selector(self.app_relaunch, signature=b"v@:@"),
		#	 "NSApplicationDidChangeScreenParametersNotification", None  # 监听屏幕变化
		# )
		return self

	def stop_listening(self):
		nc = NSWorkspace.sharedWorkspace().notificationCenter()
		nc.removeObserver_(self)

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
			if info is None:
				# 最终确认失败才跳出逻辑，避免崩溃和死循环
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write("info is still None after retry.\n")
				return  # ❗这里不要继续执行，直接退出函数
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

			mouse_location = Quartz.NSEvent.mouseLocation()

			# judge
			self.dock_postion = codecs.open(pos_file, 'r', encoding='utf-8').read()
			screens = NSScreen.screens()
			for i, screen in enumerate(screens):
				frame = screen.frame()
				x, y, w, h = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height

				if x <= mouse_location.x < x + w and y <= mouse_location.y < y + h:
					screen_position = f"{i} ({int(w)}x{int(h)})"
					print(screen_position)
					need_re_calculate = codecs.open(BasePath + "Screen2.txt", 'r', encoding='utf-8').read()
					if need_re_calculate == '1':
						try:
							if self.dock_postion == 'x':
								CMD = '''
									on run argv
										display notification (item 2 of argv) with title (item 1 of argv)
									end run'''
								self.notify(CMD, "Shameplant: Dynamically Hide Your Dock",
											f"Please go to the Settings panel in the menu bar.")
							else:
								with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
									f0.write('0')
								with open(BasePath + "Screen.txt", 'w', encoding='utf-8') as f0:
									f0.write(screen_position)
								os.execv(sys.executable, [sys.executable, __file__])
						except Exception as e:
							# 发生异常时打印错误信息
							p = "程序发生异常re1:" + str(e)
							with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
								f0.write(p)
							with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
								f0.write('1')
					if need_re_calculate == '0':
						screen_position_old = codecs.open(BasePath + "Screen.txt", 'r', encoding='utf-8').read()
						if screen_position_old == '':
							with open(BasePath + "Screen.txt", 'w', encoding='utf-8') as f0:
								f0.write(screen_position)
						else:
							if screen_position_old != screen_position:
								try:
									if self.dock_postion == 'x':
										CMD = '''
											on run argv
												display notification (item 2 of argv) with title (item 1 of argv)
											end run'''
										self.notify(CMD, "Shameplant: Dynamically Hide Your Dock",
													f"Please go to the Settings panel in the menu bar.")
									else:
										with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
											f0.write('0')
										with open(BasePath + "Screen.txt", 'w', encoding='utf-8') as f0:
											f0.write(screen_position)
										os.execv(sys.executable, [sys.executable, __file__])
								except Exception as e:
									# 发生异常时打印错误信息
									p = "程序发生异常re0:" + str(e)
									with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
										f0.write(p)
									with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
										f0.write('1')
					break
		except Exception as e:
			# 发生异常时打印错误信息
			p = "程序发生异常large:" + str(e)
			traceback_str = traceback.format_exc()
			with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
				f0.write(p + traceback_str)
			os.execv(sys.executable, [sys.executable, __file__])

	# def get_pid_psutil(self, app_name):
	#	 for proc in psutil.process_iter(attrs=["pid", "name"]):
	#		 try:
	#			 if app_name.lower() in proc.info["name"].lower():
	#				 return proc.info["pid"]
	#		 except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
	#			 continue
	#	 return None

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
	#	 sys.exit(0)

	# def restart_program(self):
	#	 subprocess.Popen([sys.executable] + sys.argv)
	#	 os._exit(0)  # 直接退出当前进程


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


class window3(QWidget):  # 主窗口
	def __init__(self):
		super().__init__()
		self.initUI()
		self.ReLa()
	
	def initUI(self):
		home_dir = str(Path.home())
		tarname1 = "ShameplantAppPath"
		fulldir1 = os.path.join(home_dir, tarname1)
		if not os.path.exists(fulldir1):
			os.mkdir(fulldir1)
		tarname2 = "Position.txt"
		self.fulldir2 = os.path.join(fulldir1, tarname2)
		if not os.path.exists(self.fulldir2):
			with open(self.fulldir2, 'a', encoding='utf-8') as f0:
				f0.write('x')
		tarname3 = "Distance.txt"
		self.fulldir3 = os.path.join(fulldir1, tarname3)
		if not os.path.exists(self.fulldir3):
			with open(self.fulldir3, 'a', encoding='utf-8') as f0:
				f0.write('0')
		tarname4 = "Launch.txt"
		self.fulldir4 = os.path.join(fulldir1, tarname4)
		if not os.path.exists(self.fulldir4):
			with open(self.fulldir4, 'a', encoding='utf-8') as f0:
				f0.write('0')
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
		tarname8 = "New.txt"
		self.fulldir8 = os.path.join(fulldir1, tarname8)
		if not os.path.exists(self.fulldir8):
			with open(self.fulldir8, 'a', encoding='utf-8') as f0:
				f0.write('0')

		###

		main_screen = NSScreen.mainScreen()
		frame = main_screen.frame()
		visible_frame = main_screen.visibleFrame()
		self.dock_postion = codecs.open(self.fulldir2, 'r', encoding='utf-8').read()
		self.auto_launch = codecs.open(self.fulldir4, 'r', encoding='utf-8').read()

		if self.dock_postion == 'x':
			CMD = '''
		        on run argv
		            display notification (item 2 of argv) with title (item 1 of argv)
		        end run'''
			self.notify(CMD, "Shameplant: Dynamically Hide Your Dock",
						f"Please go to the Settings panel in the menu bar.")
		if self.dock_postion == '0':
			# AppleScript命令
			toggle_dock_script = '''
		        tell application "System Events" to set the autohide of dock preferences to false
		    '''
			# 运行AppleScript
			subprocess.run(["osascript", "-e", toggle_dock_script])
			time.sleep(1)
			dock_height = int(visible_frame.origin.y)
			if dock_height == 0:
				os.execv(sys.executable, [sys.executable, __file__])
			menubar_height = int(frame.size.height - visible_frame.size.height - dock_height)
			core_value = int(frame.size.height - dock_height)
			# 写入记录
			with open(BasePath + "menu_height.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(menubar_height))
			with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(dock_height))
			with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(core_value))
			with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
				f0.write('0')
		if self.dock_postion == '1':
			# AppleScript命令
			toggle_dock_script = '''
		        tell application "System Events" to set the autohide of dock preferences to false
		    '''
			# 运行AppleScript
			subprocess.run(["osascript", "-e", toggle_dock_script])
			time.sleep(1)
			dock_height = int(visible_frame.origin.x - frame.origin.x)
			if dock_height == 0:
				os.execv(sys.executable, [sys.executable, __file__])
			# 写入记录
			with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(dock_height))
			with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(dock_height))
			with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
				f0.write('0')
		if self.dock_postion == '2':
			# AppleScript命令
			toggle_dock_script = '''
		        tell application "System Events" to set the autohide of dock preferences to false
		    '''
			# 运行AppleScript
			subprocess.run(["osascript", "-e", toggle_dock_script])
			time.sleep(1)
			dock_height = int(frame.size.width - visible_frame.size.width)
			if dock_height == 0:
				os.execv(sys.executable, [sys.executable, __file__])
			core_value = int(visible_frame.size.width)
			# 写入记录
			with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(dock_height))
			with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
				f0.write(str(core_value))
			with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
				f0.write('0')

		if self.auto_launch == '1':
			# launch helper
			try:
				self.listener = AppEventListener.alloc().init() # window switch auto
				# 启动鼠标监听线程 click drag auto
				self.last_active_name = None
				self.pass_key = 0
				self.mouse_thread = MouseClickListener()
				self.mouse_thread.click_signal.connect(self.on_click_action)
				self.mouse_thread.drag_signal.connect(self.update_label)
				self.mouse_thread.start()
				action3.setChecked(True)
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
				action3.setChecked(False)

		# 启动计时线程
		self.timer_thread = TimerThread()
		self.timer_thread.tick.connect(self.on_timer_tick)
		self.timer_thread.start()

		# Guide
		new_guide = codecs.open(self.fulldir8, 'r', encoding='utf-8').read()
		if new_guide == '0':
			w5.show()

	def notify(self, CMD, title, text):
		subprocess.call(['osascript', '-e', CMD, title, text])

	def activate(self):  # 设置窗口显示
		if action3.isChecked():
			# launch helper
			try:
				self.listener = AppEventListener.alloc().init()  # window switch auto
				# 启动鼠标监听线程 click drag auto
				self.last_active_name = None
				self.pass_key = 0
				self.mouse_thread = MouseClickListener()
				self.mouse_thread.click_signal.connect(self.on_click_action)
				self.mouse_thread.drag_signal.connect(self.update_label)
				self.mouse_thread.start()
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
				action3.setChecked(False)
		if not action3.isChecked():
			try:
				if self.listener:
					self.listener.stop_listening() # window switch auto
				# 启动鼠标监听线程 click drag auto
				if self.mouse_thread:
					self.mouse_thread.stop()
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)

	def ReLa(self):
		ReLa = codecs.open(BasePath + "ReLa.txt", 'r', encoding='utf-8').read()
		if ReLa == '1':
			try:
				self.listener = AppEventListener.alloc().init()  # window switch auto
				# 启动鼠标监听线程 click drag auto
				self.last_active_name = None
				self.pass_key = 0
				self.mouse_thread = MouseClickListener()
				self.mouse_thread.click_signal.connect(self.on_click_action)
				self.mouse_thread.drag_signal.connect(self.update_label)
				self.mouse_thread.start()
				action3.setChecked(True)
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
				action3.setChecked(False)

	def get_screen_with_dock(self):
		for screen in NSScreen.screens():
			frame = screen.frame()
			visible = screen.visibleFrame()

			# Dock 在底部时 visibleFrame 的 origin.y 会 > frame.origin.y
			if visible.origin.y > frame.origin.y:
				dock_height = visible.origin.y - frame.origin.y
				return {
					"screen": screen,
					"dock_position": "bottom",
					"dock_height": dock_height
				}

			# Dock 在左边
			if visible.origin.x > frame.origin.x:
				dock_height = visible.origin.x - frame.origin.x
				#print(visible.origin.x, frame.origin.x)
				return {"screen": screen,
						"dock_position": "left",
						"dock_height": dock_height
						}

			# Dock 在右边
			if visible.size.width < frame.size.width:
				dock_height = frame.size.width - visible.size.width
				return {"screen": screen,
						"dock_position": "right",
						"dock_height": dock_height
						}

		return None
	def on_timer_tick(self):
		# 如果此时的dock有显示、不为None，且dock的高度不为0，那么更新本地记录
		if self.get_screen_with_dock() != None:
			main_screen = NSScreen.mainScreen()
			frame = main_screen.frame()
			visible_frame = main_screen.visibleFrame()
			try:
				if self.dock_postion == 'x':
					CMD = '''
				        on run argv
				            display notification (item 2 of argv) with title (item 1 of argv)
				        end run'''
					self.notify(CMD, "Shameplant: Dynamically Hide Your Dock",
								f"Please go to the Settings panel in the menu bar.")
				if self.dock_postion == '0':
					# AppleScript命令
					toggle_dock_script = '''
				        tell application "System Events" to set the autohide of dock preferences to false
				    '''
					# 运行AppleScript
					subprocess.run(["osascript", "-e", toggle_dock_script])
					time.sleep(1)
					dock_height = int(visible_frame.origin.y)
					menubar_height = int(frame.size.height - visible_frame.size.height - dock_height)
					core_value = int(frame.size.height - dock_height)
					if dock_height > 0:
						# 写入记录
						with open(BasePath + "menu_height.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(menubar_height))
						with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(dock_height))
						with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(core_value))
						with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
							f0.write('0')
				if self.dock_postion == '1':
					# AppleScript命令
					toggle_dock_script = '''
				        tell application "System Events" to set the autohide of dock preferences to false
				    '''
					# 运行AppleScript
					subprocess.run(["osascript", "-e", toggle_dock_script])
					time.sleep(1)
					dock_height = int(visible_frame.origin.x - frame.origin.x)
					if dock_height > 0:
						# 写入记录
						with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(dock_height))
						with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(dock_height))
						with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
							f0.write('0')
				if self.dock_postion == '2':
					# AppleScript命令
					toggle_dock_script = '''
				        tell application "System Events" to set the autohide of dock preferences to false
				    '''
					# 运行AppleScript
					subprocess.run(["osascript", "-e", toggle_dock_script])
					time.sleep(1)
					dock_height = int(frame.size.width - visible_frame.size.width)
					core_value = int(visible_frame.size.width)
					if dock_height > 0:
						# 写入记录
						with open(BasePath + "dock_height.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(dock_height))
						with open(BasePath + "core_value.txt", 'w', encoding='utf-8') as f0:
							f0.write(str(core_value))
						with open(BasePath + "Screen2.txt", 'w', encoding='utf-8') as f0:
							f0.write('0')
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
		else:
			pass

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
				if info is None:
					# 最终确认失败才跳出逻辑，避免崩溃和死循环
					with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
						f0.write("info is still None after retry.\n")
					return  # ❗这里不要继续执行，直接退出函数
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

	def update_label(self, x, y):
		try:
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
			if info is None:
				# 最终确认失败才跳出逻辑，避免崩溃和死循环
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write("info is still None after retry.\n")
				return  # ❗这里不要继续执行，直接退出函数
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

	def login_start(self):
		plist_filename = 'com.ryanthehito.shameplant.plist'
		if action10.isChecked():
			try:
				launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
				launch_agents_dir.mkdir(parents=True, exist_ok=True)
				plist_source_path = BasePath + plist_filename
				destination = launch_agents_dir / plist_filename
				shutil.copy2(plist_source_path, destination)
				# 设置权限确保 macOS 能读
				os.chmod(destination, 0o644)
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常: Autostart failed: " + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
		if not action3.isChecked():
			try:
				plist_path = Path.home() / "Library" / "LaunchAgents" / plist_filename
				if plist_path.exists():
					# 删除文件
					plist_path.unlink()
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常: Removing autostart failed: " + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)


class window4(QWidget):  # Customization settings
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):  # 设置窗口内布局
		self.setUpMainWindow()
		self.setFixedSize(500, 870)
		self.center()
		self.setWindowTitle('Customization settings')
		self.setFocus()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

		dock_position = codecs.open(self.fulldir2, 'r', encoding='utf-8').read()
		if dock_position == 'x':
			self.show()
			self.setFocus()
			self.raise_()
			self.activateWindow()

	def setUpMainWindow(self):
		home_dir = str(Path.home())
		tarname1 = "ShameplantAppPath"
		fulldir1 = os.path.join(home_dir, tarname1)
		if not os.path.exists(fulldir1):
			os.mkdir(fulldir1)
		tarname2 = "Position.txt"
		self.fulldir2 = os.path.join(fulldir1, tarname2)
		if not os.path.exists(self.fulldir2):
			with open(self.fulldir2, 'a', encoding='utf-8') as f0:
				f0.write('x')
		tarname3 = "Distance.txt"
		self.fulldir3 = os.path.join(fulldir1, tarname3)
		if not os.path.exists(self.fulldir3):
			with open(self.fulldir3, 'a', encoding='utf-8') as f0:
				f0.write('0')
		tarname4 = "Launch.txt"
		self.fulldir4 = os.path.join(fulldir1, tarname4)
		if not os.path.exists(self.fulldir4):
			with open(self.fulldir4, 'a', encoding='utf-8') as f0:
				f0.write('0')
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
		tarname8 = "New.txt"
		self.fulldir8 = os.path.join(fulldir1, tarname8)
		if not os.path.exists(self.fulldir8):
			with open(self.fulldir8, 'a', encoding='utf-8') as f0:
				f0.write('0')

		###

		self.lbl1 = QLabel('Dock position: ', self)

		self.box_position = QComboBox(self)
		self.box_position.setEditable(False)
		self.box_position.setFixedWidth(370)
		defalist = ['Bottom', 'Left', 'Right']
		self.box_position.addItems(defalist)
		if self.get_screen_with_dock() != None:
			if self.get_screen_with_dock() == '0':
				self.box_position.setCurrentIndex(0)
				with open(self.fulldir2, 'w', encoding='utf-8') as f0:
					f0.write('0')
			if self.get_screen_with_dock() == '1':
				self.box_position.setCurrentIndex(1)
				with open(self.fulldir2, 'w', encoding='utf-8') as f0:
					f0.write('1')
			if self.get_screen_with_dock() == '2':
				self.box_position.setCurrentIndex(2)
				with open(self.fulldir2, 'w', encoding='utf-8') as f0:
					f0.write('2')
		self.box_position.currentIndexChanged.connect(self.position_change)

		self.lbl2 = QLabel('Threshold: ', self)

		self.le1 = QLineEdit(self)
		self.le1.setFixedWidth(360)
		self.le1.setPlaceholderText('Pixel(s). Numbers only, no decimal. Default=0')
		text = codecs.open(self.fulldir3, 'r', encoding='utf-8').read()
		self.le1.setText(text)

		self.checkBox1 = QCheckBox('Start when app launches', self)
		LastCert = codecs.open(self.fulldir4, 'r', encoding='utf-8').read()
		if LastCert == '1':
			self.checkBox1.setChecked(True)
		if LastCert == '0':
			self.checkBox1.setChecked(False)
		self.checkBox1.clicked.connect(self.auto_launch)

		###

		lbl0 = QLabel("Don't react to:", self)

		self.text_feed = QListWidget(self)
		self.text_feed.setFixedHeight(200)
		self.text_feed.itemSelectionChanged.connect(self.item_click_0)

		self.btn0_1 = QPushButton('', self)
		self.btn0_1.setFixedSize(15, 15)
		btn0_1_path = BasePath + 'plus.png'
		self.btn0_1.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn0_1_path)
		self.btn0_1.move(30, 320)

		self.btn0_2 = QPushButton('', self)
		self.btn0_2.setFixedSize(15, 15)
		btn0_2_path = BasePath + 'minus.png'
		self.btn0_2.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn0_2_path)
		self.btn0_2.move(55, 320)
		self.btn0_2.setVisible(False)

		###

		lbl1 = QLabel("Always show Dock for:", self)

		self.text_feed_1 = QListWidget(self)
		self.text_feed_1.setFixedHeight(200)
		self.text_feed_1.itemSelectionChanged.connect(self.item_click_1)

		self.btn1_1 = QPushButton('', self)
		self.btn1_1.setFixedSize(15, 15)
		btn1_1_path = BasePath + 'plus.png'
		self.btn1_1.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn1_1_path)
		self.btn1_1.move(30, 555)

		self.btn1_2 = QPushButton('', self)
		self.btn1_2.setFixedSize(15, 15)
		btn1_2_path = BasePath + 'minus.png'
		self.btn1_2.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn1_2_path)
		self.btn1_2.move(55, 555)
		self.btn1_2.setVisible(False)

		###

		lbl2 = QLabel("Always hide Dock for:", self)

		self.text_feed_2 = QListWidget(self)
		self.text_feed_2.setFixedHeight(200)
		self.text_feed_2.itemSelectionChanged.connect(self.item_click_2)

		self.btn2_1 = QPushButton('', self)
		self.btn2_1.setFixedSize(15, 15)
		btn2_1_path = BasePath + 'plus.png'
		self.btn2_1.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn2_1_path)
		self.btn2_1.move(30, 790)

		self.btn2_2 = QPushButton('', self)
		self.btn2_2.setFixedSize(15, 15)
		btn2_2_path = BasePath + 'minus.png'
		self.btn2_2.setStyleSheet('''
			QPushButton{
			border: transparent;
			background-color: transparent;
			border-image: url(%s);
			}
			QPushButton:pressed{
			border: 1px outset grey;
			background-color: #0085FF;
			border-radius: 4px;
			padding: 1px;
			color: #FFFFFF
			}
			''' % btn2_2_path)
		self.btn2_2.move(55, 790)

		self.btn_1 = QPushButton('Save and relaunch', self)
		self.btn_1.clicked.connect(self.save_state)
		self.btn_1.setFixedSize(150, 20)

		###

		qw0 = QWidget()
		vbox0 = QHBoxLayout()
		vbox0.setContentsMargins(0, 0, 0, 0)
		vbox0.addWidget(self.lbl1)
		vbox0.addWidget(self.box_position)
		qw0.setLayout(vbox0)

		qw1 = QWidget()
		vbox1 = QHBoxLayout()
		vbox1.setContentsMargins(0, 0, 0, 0)
		vbox1.addWidget(self.lbl2)
		vbox1.addWidget(self.le1)
		qw1.setLayout(vbox1)

		qw2 = QWidget()
		vbox2 = QHBoxLayout()
		vbox2.setContentsMargins(0, 0, 0, 0)
		vbox2.addWidget(self.checkBox1)
		qw2.setLayout(vbox2)

		qw4 = QWidget()
		vbox4 = QVBoxLayout()
		vbox4.setContentsMargins(0, 0, 0, 0)
		vbox4.addWidget(lbl0)
		vbox4.addWidget(self.text_feed)
		vbox4.addWidget(lbl1)
		vbox4.addWidget(self.text_feed_1)
		vbox4.addWidget(lbl2)
		vbox4.addWidget(self.text_feed_2)
		vbox4.addStretch()
		qw4.setLayout(vbox4)

		qw3 = QWidget()
		vbox3 = QHBoxLayout()
		vbox3.setContentsMargins(0, 0, 0, 0)
		vbox3.addStretch()
		vbox3.addWidget(self.btn_1)
		vbox3.addStretch()
		qw3.setLayout(vbox3)

		vboxx = QVBoxLayout()
		vboxx.setContentsMargins(20, 20, 20, 20)
		vboxx.addWidget(qw0)
		vboxx.addWidget(qw1)
		vboxx.addWidget(qw2)
		vboxx.addWidget(qw4)
		vboxx.addWidget(qw3)
		self.setLayout(vboxx)

		self.btn0_1.raise_()
		self.btn0_2.raise_()
		self.btn1_1.raise_()
		self.btn1_2.raise_()
		self.btn2_1.raise_()
		self.btn2_2.raise_()

		never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read()
		never_react_list = never_react.split('\n')
		while '' in never_react_list:
			never_react_list.remove('')
		self.text_feed.clear()
		self.text_feed.addItems(never_react_list)

		always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read()
		always_show_list = always_show.split('\n')
		while '' in always_show_list:
			always_show_list.remove('')
		self.text_feed_1.clear()
		self.text_feed_1.addItems(always_show_list)

		never_show = codecs.open(self.fulldir7, 'r', encoding='utf-8').read()
		never_show_list = never_show.split('\n')
		while '' in never_show_list:
			never_show_list.remove('')
		self.text_feed_2.clear()
		self.text_feed_2.addItems(never_show_list)

	def item_click_0(self):
		selected_items = self.text_feed.selectedItems()  # 获取已选择的项
		if len(selected_items) > 0:
			pass
			self.btn0_2.setVisible(True)
		else:
			pass
			self.btn0_2.setVisible(False)

	def item_click_1(self):
		selected_items = self.text_feed_1.selectedItems()  # 获取已选择的项
		if len(selected_items) > 0:
			pass
			self.btn1_2.setVisible(True)
		else:
			pass
			self.btn1_2.setVisible(False)

	def item_click_2(self):
		selected_items = self.text_feed_2.selectedItems()  # 获取已选择的项
		if len(selected_items) > 0:
			pass
			self.btn2_2.setVisible(True)
		else:
			pass
			self.btn2_2.setVisible(False)

	def add_item_0(self):
		fj = QFileDialog.getOpenFileName(self, "Open File", str(Path("/Applications")), "Application (*.app)")
		if fj[0] != '':
			pattern2 = re.compile(r'([^/]+)\.app$')
			result = ''.join(pattern2.findall(fj[0])) + '\n'
			never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read()
			never_react_list = never_react.split('\n')
			while '' in never_react_list:
				never_react_list.remove('')
			if result.rstrip('\n') not in never_react_list:
				with open(self.fulldir5, 'a', encoding='utf-8') as f0:
					f0.write(result)
				never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read().lstrip('\n')
				with open(self.fulldir5, 'w', encoding='utf-8') as f0:
					f0.write(never_react)
			never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read()
			never_react_list = never_react.split('\n')
			while '' in never_react_list:
				never_react_list.remove('')
			self.text_feed.clear()
			self.text_feed.addItems(never_react_list)

	def delete_item_0(self):
		selected_items = self.text_feed.selectedItems()
		if len(selected_items) > 0:
			index = 0
			text = ''
			for item in selected_items:
				index = self.text_feed.row(item)  # 获取选中项的索引
				text = item.text()
			output_list = []
			for i in range(self.text_feed.count()):
				output_list.append(self.text_feed.item(i).text())
			while '' in output_list:
				output_list.remove('')
			if text != '':
				deletelist = []
				deletelist.append(output_list[index])
				output_list.remove(deletelist[0])
				#set show
				self.text_feed.clear()
				self.text_feed.addItems(output_list)
				# write to local
				output = '\n'.join(output_list) + '\n'
				with open(self.fulldir5, 'w', encoding='utf-8') as f0:
					f0.write('')
				with open(self.fulldir5, 'w', encoding='utf-8') as f0:
					f0.write(output)

	def add_item_1(self):
		fj = QFileDialog.getOpenFileName(self, "Open File", str(Path("/Applications")), "Application (*.app)")
		if fj[0] != '':
			pattern2 = re.compile(r'([^/]+)\.app$')
			result = ''.join(pattern2.findall(fj[0])) + '\n'
			always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read()
			always_show_list = always_show.split('\n')
			while '' in always_show_list:
				always_show_list.remove('')
			if result.rstrip('\n') not in always_show_list:
				with open(self.fulldir6, 'a', encoding='utf-8') as f0:
					f0.write(result)
				always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read().lstrip('\n')
				with open(self.fulldir6, 'w', encoding='utf-8') as f0:
					f0.write(always_show)
			always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read()
			always_show_list = always_show.split('\n')
			while '' in always_show_list:
				always_show_list.remove('')
			self.text_feed_1.clear()
			self.text_feed_1.addItems(always_show_list)

	def delete_item_1(self):
		selected_items = self.text_feed_1.selectedItems()
		if len(selected_items) > 0:
			index = 0
			text = ''
			for item in selected_items:
				index = self.text_feed_1.row(item)  # 获取选中项的索引
				text = item.text()
			output_list = []
			for i in range(self.text_feed_1.count()):
				output_list.append(self.text_feed_1.item(i).text())
			while '' in output_list:
				output_list.remove('')
			if text != '':
				deletelist = []
				deletelist.append(output_list[index])
				output_list.remove(deletelist[0])
				#set show
				self.text_feed_1.clear()
				self.text_feed_1.addItems(output_list)
				# write to local
				output = '\n'.join(output_list) + '\n'
				with open(self.fulldir6, 'w', encoding='utf-8') as f0:
					f0.write('')
				with open(self.fulldir6, 'w', encoding='utf-8') as f0:
					f0.write(output)

	def add_item_2(self):
		fj = QFileDialog.getOpenFileName(self, "Open File", str(Path("/Applications")), "Application (*.app)")
		if fj[0] != '':
			pattern2 = re.compile(r'([^/]+)\.app$')
			result = ''.join(pattern2.findall(fj[0])) + '\n'
			never_show = codecs.open(self.fulldir7, 'r', encoding='utf-8').read()
			never_show_list = never_show.split('\n')
			while '' in never_show_list:
				never_show_list.remove('')
			if result.rstrip('\n') not in never_show_list:
				with open(self.fulldir7, 'a', encoding='utf-8') as f0:
					f0.write(result)
				never_show = codecs.open(self.fulldir7, 'r', encoding='utf-8').read().lstrip('\n')
				with open(self.fulldir7, 'w', encoding='utf-8') as f0:
					f0.write(never_show)
			never_show = codecs.open(self.fulldir7, 'r', encoding='utf-8').read()
			never_show_list = never_show.split('\n')
			while '' in never_show_list:
				never_show_list.remove('')
			self.text_feed_2.clear()
			self.text_feed_2.addItems(never_show_list)

	def delete_item_2(self):
		selected_items = self.text_feed_2.selectedItems()
		if len(selected_items) > 0:
			index = 0
			text = ''
			for item in selected_items:
				index = self.text_feed_2.row(item)  # 获取选中项的索引
				text = item.text()
			output_list = []
			for i in range(self.text_feed_2.count()):
				output_list.append(self.text_feed_2.item(i).text())
			while '' in output_list:
				output_list.remove('')
			if text != '':
				deletelist = []
				deletelist.append(output_list[index])
				output_list.remove(deletelist[0])
				#set show
				self.text_feed_2.clear()
				self.text_feed_2.addItems(output_list)
				# write to local
				output = '\n'.join(output_list) + '\n'
				with open(self.fulldir7, 'w', encoding='utf-8') as f0:
					f0.write('')
				with open(self.fulldir7, 'w', encoding='utf-8') as f0:
					f0.write(output)

	def position_change(self, i):
		if i == 0:
			cmd = """
				tell application "System Events"
					do shell script "defaults write com.apple.dock orientation -string bottom; killall Dock"
				end tell"""
			try:
				subprocess.call(['osascript', '-e', cmd])
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
			with open(self.fulldir2, 'w', encoding='utf-8') as f0:
				f0.write('0')
		if i == 1:
			cmd = """
				tell application "System Events"
					do shell script "defaults write com.apple.dock orientation -string left; killall Dock"
				end tell"""
			try:
				subprocess.call(['osascript', '-e', cmd])
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
			with open(self.fulldir2, 'w', encoding='utf-8') as f0:
				f0.write('0')
			with open(self.fulldir2, 'w', encoding='utf-8') as f0:
				f0.write('1')
		if i == 2:
			cmd = """
				tell application "System Events"
					do shell script "defaults write com.apple.dock orientation -string right; killall Dock"
				end tell"""
			try:
				subprocess.call(['osascript', '-e', cmd])
			except Exception as e:
				# 发生异常时打印错误信息
				p = "程序发生异常:" + str(e)
				with open(BasePath + "Error.txt", 'a', encoding='utf-8') as f0:
					f0.write(p)
			with open(self.fulldir2, 'w', encoding='utf-8') as f0:
				f0.write('0')
			with open(self.fulldir2, 'w', encoding='utf-8') as f0:
				f0.write('2')

	def auto_launch(self):
		if self.checkBox1.isChecked():
			with open(self.fulldir4, 'w', encoding='utf-8') as f0:
				f0.write('1')
		else:
			with open(self.fulldir4, 'w', encoding='utf-8') as f0:
				f0.write('0')

	def save_state(self):
		with open(self.fulldir2, 'w', encoding='utf-8') as f0:
			f0.write(str(self.box_position.currentIndex()))
		if self.le1.text() != '':
			with open(self.fulldir3, 'w', encoding='utf-8') as f0:
				f0.write(str(self.le1.text()))
		self.close()
		with open(BasePath + "DockRe.txt", 'w', encoding='utf-8') as f0:
			f0.write('0')
		with open(BasePath + "ReLa.txt", 'w', encoding='utf-8') as f0:
			f0.write('1')
		time.sleep(0.5)
		os.execv(sys.executable, [sys.executable, __file__])

	def get_screen_with_dock(self):
		for screen in NSScreen.screens():
			frame = screen.frame()
			visible = screen.visibleFrame()
			# Dock 在底部时 visibleFrame 的 origin.y 会 > frame.origin.y
			if visible.origin.y > frame.origin.y:
				return '0'
			# Dock 在左边
			if visible.origin.x > frame.origin.x:
				return '1'
			# Dock 在右边
			if visible.size.width < frame.size.width:
				return '2'
		return None

	def totalquit(self):
		with open(BasePath + "ReLa.txt", 'w', encoding='utf-8') as f0:
			f0.write('0')
		if action3.isChecked():
			if w3.listener:
				w3.listener.stop_listening()  # window switch auto
			# 启动鼠标监听线程 click drag auto
			if w3.mouse_thread:
				w3.mouse_thread.stop()
		sys.exit(0)

	def restart(self):
		if w3.listener:
			w3.listener.stop_listening()  # window switch auto
		# 启动鼠标监听线程 click drag auto
		if w3.mouse_thread:
			w3.mouse_thread.stop()
		time.sleep(3)
		os.execv(sys.executable, [sys.executable, __file__])
	
	def center(self):  # 设置窗口居中
		qr = self.frameGeometry()
		cp = self.screen().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def keyPressEvent(self, e):  # 当页面显示的时候，按下esc键可关闭窗口
		if e.key() == Qt.Key.Key_Escape.value:
			self.close()
	
	def activate(self):  # 设置窗口显示
		w2.checkupdate()
		if w2.lbl2.text() != 'No Intrenet' and 'ready' in w2.lbl2.text():
			w2.show()

		never_react = codecs.open(self.fulldir5, 'r', encoding='utf-8').read()
		never_react_list = never_react.split('\n')
		while '' in never_react_list:
			never_react_list.remove('')
		self.text_feed.clear()
		self.text_feed.addItems(never_react_list)

		always_show = codecs.open(self.fulldir6, 'r', encoding='utf-8').read()
		always_show_list = always_show.split('\n')
		while '' in always_show_list:
			always_show_list.remove('')
		self.text_feed_1.clear()
		self.text_feed_1.addItems(always_show_list)

		never_show = codecs.open(self.fulldir7, 'r', encoding='utf-8').read()
		never_show_list = never_show.split('\n')
		while '' in never_show_list:
			never_show_list.remove('')
		self.text_feed_2.clear()
		self.text_feed_2.addItems(never_show_list)

		self.show()
		self.setFocus()
		self.raise_()
		self.activateWindow()
	
	def cancel(self):  # 设置取消键的功能
		self.close()

style_sheet_ori = '''
	QTabWidget::pane {
		border: 1px solid #ECECEC;
		background: #ECECEC;
		border-radius: 9px;
}
	QTableWidget{
		border: 1px solid grey;  
		border-radius:4px;
		background-clip: border;
		background-color: #FFFFFF;
		color: #000000;
		font: 14pt Helvetica;
}
	QWidget#Main {
		border: 1px solid #ECECEC;
		background: #ECECEC;
		border-radius: 9px;
}
	QPushButton{
		border: 1px outset grey;
		background-color: #FFFFFF;
		border-radius: 4px;
		padding: 1px;
		color: #000000
}
	QPushButton:pressed{
		border: 1px outset grey;
		background-color: #0085FF;
		border-radius: 4px;
		padding: 1px;
		color: #FFFFFF
}
	QPlainTextEdit{
		border: 1px solid grey;  
		border-radius:4px;
		padding: 1px 5px 1px 3px; 
		background-clip: border;
		background-color: #F3F2EE;
		color: #000000;
		font: 14pt Times New Roman;
}
	QPlainTextEdit#edit{
		border: 1px solid grey;  
		border-radius:4px;
		padding: 1px 5px 1px 3px; 
		background-clip: border;
		background-color: #FFFFFF;
		color: rgb(113, 113, 113);
		font: 14pt Helvetica;
}
	QTableWidget#small{
		border: 1px solid grey;  
		border-radius:4px;
		background-clip: border;
		background-color: #F3F2EE;
		color: #000000;
		font: 14pt Times New Roman;
}
	QLineEdit{
		border-radius:4px;
		border: 1px solid gray;
		background-color: #FFFFFF;
}
	QTextEdit{
		border: 1px solid grey;  
		border-radius:4px;
		padding: 1px 5px 1px 3px; 
		background-clip: border;
		background-color: #F3F2EE;
		color: #000000;
		font: 14pt Times New Roman;
}
	QListWidget{
		border: 1px solid grey;  
		border-radius:4px;
		padding: 1px 5px 1px 3px; 
		background-clip: border;
		background-color: #F3F2EE;
		color: #000000;
		font: 14pt Times New Roman;
}
'''

if __name__ == '__main__':
	while True:
		try:
			w1 = window_about()  # about
			w2 = window_update()  # update
			w4 = window4()  # CUSTOMIZING
			w5 = SliderWindow() # guide
			w5.setAutoFillBackground(True)
			p = w5.palette()
			p.setColor(w5.backgroundRole(), QColor('#ECECEC'))
			w5.setPalette(p)
			w3 = window3()  # main1
			w3.setAutoFillBackground(True)
			p = w3.palette()
			p.setColor(w3.backgroundRole(), QColor('#ECECEC'))
			w3.setPalette(p)
			action1.triggered.connect(w1.activate)
			action2.triggered.connect(w2.activate)
			action3.triggered.connect(w3.activate)
			action7.triggered.connect(w4.activate)
			action8.triggered.connect(w4.restart)
			action9.triggered.connect(w5.show)
			action10.triggered.connect(w3.login_start)
			btna4.triggered.connect(w3.activate)
			btna5.triggered.connect(w4.activate)
			btna6.triggered.connect(w4.totalquit)
			w4.btn0_1.clicked.connect(w4.add_item_0)
			w4.btn0_2.clicked.connect(w4.delete_item_0)
			w4.btn1_1.clicked.connect(w4.add_item_1)
			w4.btn1_2.clicked.connect(w4.delete_item_1)
			w4.btn2_1.clicked.connect(w4.add_item_2)
			w4.btn2_2.clicked.connect(w4.delete_item_2)
			quit.triggered.connect(w4.totalquit)
			app.setStyleSheet(style_sheet_ori)
			app.exec()
		except Exception as e:
			# 发生异常时打印错误信息
			p = "程序发生异常:" + str(e)
			with open(BasePath + "Error.txt", 'w', encoding='utf-8') as f0:
				f0.write(p)
			# 延时一段时间后重新启动程序（例如延时 5 秒）
			time.sleep(5)
			# 重启后的操作
			with open(BasePath + "ReLa.txt", 'w', encoding='utf-8') as f0:
				f0.write('1')
			# 使用 os.execv() 在当前进程中启动自身，实现自动重启
			os.execv(sys.executable, [sys.executable, __file__])
