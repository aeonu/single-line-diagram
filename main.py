# cython: language_level=3
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Date    : 2022-10-25 00:23:45
# @Function: Auto-drawing single line diagram
# @Author  : Luo Xiaochun
# @Email   : luoxiaochun@proton.me
# @version : 1.1.0


import time
import sys
import win32api
import win32con
import wmi
import wx
from disgrama import Disframe


class App(wx.App):
    def OnInit(self):

        # frame1 = LoginFrame()
        # frame1.Show()
        grame = Disframe(None)
        grame.Show()

        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
