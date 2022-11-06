# cython: language_level=3
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Date    : 2022-10-25 00:23:45
# @Function: Auto-drawing single line diagram
# @Author  : Luo Xiaochun
# @Email   : luoxiaochun@proton.me
# @version : 1.1.0

import wx
from matplotlib import markers
from matplotlib.path import Path
import settings
import math
import numpy as np
import matplotlib

matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle

import random
from flask import Flask, render_template, send_from_directory, request, abort
import sqlite3
import os
import time
import webbrowser
import base64
from pubsub import pub
import threading
from addtransz import addtransz
from single_line import polemodify
from matplotlib.text import Text




def intput_polepath(inpolepath):
    polepath_raw = inpolepath
    # polepath_raw = 'X12.F7.8.H6.Z1'
    polesplit = polepath_raw.split('.')
    for j in range(len(polesplit)):
        if 'F' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('F', 'F&'))
        if 'G' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('G', 'G&'))
        if 'H' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('H', 'H&'))
        if 'X' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('X', 'X&'))
        if 'Z' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('Z', 'Z&'))
        if 'Y' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('Y', 'Y&'))
        if 'L' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('L', 'L&'))

        if 'f' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('f', 'F&'))
        if 'g' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('g', 'G&'))
        if 'h' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('h', 'H&'))
        if 'x' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('x', 'X&'))
        if 'z' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('z', 'Z&'))
        if 'y' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('y', 'Y&'))
        if 'l' in polesplit[j]:
            polesplit[j] = (polesplit[j].replace('l', 'L&'))

    inpolepath = '.'.join(polesplit)
    return inpolepath


# inpoleact = intput_polepath('12.F7.8.H6.1')

# print('inpoleact =', inpoleact )

def output_polepath(inpolepath):
    polepath_raw = inpolepath
    # polepath_raw = 'X&12.F&7.8.H&6.Z&1'
    polesplit = polepath_raw.split('.')
    for j in range(len(polesplit)):
        if 'F' in polesplit[j] or 'G' in polesplit[j] or 'H' in polesplit[j] or 'X' in polesplit[j] or 'Z' in polesplit[
            j] or 'Y' in polesplit[j] or 'L' in polesplit[j]:
            polesplit[j] = polesplit[j].replace('&', '')
        if 'f' in polesplit[j] or 'g' in polesplit[j] or 'h' in polesplit[j] or 'x' in polesplit[j] or 'z' in polesplit[
            j] or 'y' in polesplit[j] or 'l' in polesplit[j]:
            polesplit[j] = polesplit[j].replace('&', '')
    outpolepath = '.'.join(polesplit)
    return outpolepath


# poleact = output_polepath('12.F&7.8.H&6.1')

# print('poleact=', poleact)


def onpicktext(event):
    if isinstance(event.artist, Text):
        text = event.artist
        print('onpick1 text:', text.get_text())
        l_name = settings.lname

        settings.chosen = text.get_text().replace('\n', '')
        print('settings.chosen=', settings.chosen)

        # if '-' in text.get_text():
        if '-' in text.get_text() or text.get_text()[0] =='9':
            t_capa = text.get_text()
            settings.capacity = t_capa
        else:
            t_name = text.get_text().replace('\n', '')
            settings.tname = t_name

        # print('line, tname = ', l_name, t_name)


def onclick(event):
    # print('buttonbigin=%d, xbigin=%d, ybingin=%d, xdatas=%f, ydatas=%f' %
    # (event.button, event.x, event.y, event.xdata, event.ydata))

    return event.xdata, event.ydata


cxrelease = []
cyrelease = []

txrelease = []
tyrelease = []


def anclick(event):
    print('line_name, tran_name, capa_name= ', settings.lname, settings.tname, settings.capacity, )
    print('buttonend=%d, xend=%d, yend=%d, xdataend=%f, ydataend=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    # -------------------调整坐标存入数据库Start--------------------------
    print('settings.chosen=', settings.chosen)

    # --------------------------------------------------------------------
    mlname = settings.lname
    mtrans = settings.tname

    print('settings.capacity=', settings.capacity)

    try:
        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()

        # if '-' in settings.chosen:
        if '-' in settings.chosen or settings.chosen[0]=='9':
            cxrelease.append(event.x)
            cyrelease.append(event.y)

            print('cxrelease=', cxrelease)
            print('cyrelease=', cyrelease)

            cxpoint = cxrelease[-1] - settings.cxpress[0]
            cypoint = cyrelease[-1] - settings.cypress[0]
            print('cxponit, cypoint=', cxpoint, cypoint)

            settings.cxrelease = cxrelease
            settings.cyrelease = cyrelease

            cur.execute(
                "UPDATE  transz SET xcapacity= xcapacity + (?) where tname='" + str(
                    mtrans) + "' and lname='" + str(
                    mlname) + "'", [cxpoint])
            print('-------------------------')

            cur.execute(
                "UPDATE  transz SET ycapacity= ycapacity + (?) where tname='" + str(
                    mtrans) + "' and lname='" + str(
                    mlname) + "'", [cypoint])
            print('zcapacity is change!!')

            settings.cxpress.clear()
            settings.cypress.clear()

            cxrelease.clear()
            cyrelease.clear()

            cxpoint = []
            cypoint = []
            settings.chosen = ''


        else:
            if settings.chosen:

                txrelease.append(event.x)
                tyrelease.append(event.y)

                print('txrelease=', txrelease)
                print('tyrelease=', tyrelease)

                settings.txrelease = txrelease
                settings.tyrelease = tyrelease

                txpoint = txrelease[-1] - settings.txpress[0]
                typoint = tyrelease[-1] - settings.typress[0]
                print('txponit, typoint=', txpoint, typoint)

                cur.execute(
                    "UPDATE  transz SET xtransformer= xtransformer + (?) where tname='" + str(
                        mtrans) + "' and lname='" + str(
                        mlname) + "'", [txpoint])
                cur.execute(
                    "UPDATE  transz SET ytransformer= ytransformer + (?) where tname='" + str(
                        mtrans) + "' and lname='" + str(
                        mlname) + "'", [typoint])
                print('ztransformer is change!!')

                settings.txpress.clear()
                settings.typress.clear()

                txrelease.clear()
                tyrelease.clear()

                cxpoint = []
                cypoint = []

                print('txrelease.clear()=', txrelease)
                print('tyrelease.clear()=', tyrelease)
                settings.chosen = ''

            else:
                print('not change!!')
                pass

        conn.commit()
        conn.close()





    except:
        event.button = 0
        settings.chosen = ''
        settings.tname = ''
        settings.capacity = ''
        pass

    # -------------------调整坐标存入数据库End--------------------------
    return event.xdata, event.ydata


# ----------------------------------------------------

def align_marker(marker, halign='center', valign='middle', ):
    if isinstance(halign, (str, np.unicode)):
        halign = {'right': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'left': 1.,
                  }[halign]

    if isinstance(valign, (str, np.unicode)):
        valign = {'top': -1.,
                  'middle': 0.,
                  'center': 0.,
                  'bottom': 1.,
                  }[valign]

    # Define the base marker
    bm = markers.MarkerStyle(marker)

    # Get the marker path and apply the marker transform to get the
    # actual marker vertices (they should all be in a unit-square
    # centered at (0, 0))
    m_arr = bm.get_path().transformed(bm.get_transform()).vertices

    # Shift the marker vertices for the specified alignment.
    m_arr[:, 0] += halign / 2
    m_arr[:, 1] += valign / 2

    return Path(m_arr, bm.get_path().codes)


class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.figure = Figure()
        # self.figure = Figure(figsize=(9.2, 4.75))

        # self.figure = Figure(figsize=(13.2, 5.75))
        #  self.figure = Figure(figsize=(17.2, 7.65))
        self.SetBackgroundColour('#f5f5d5')
        # 笔记本
        # self.figure = Figure(dpi=80, figsize=(17.2, 8.45))
        self.figure = Figure(dpi=80, figsize=(21, 13))
        # self.figure = Figure(dpi=72, figsize=(18.97, 9.45))
        # self.axes = self.figure.add_subplot(111)
        self.axes = self.figure.add_axes([0.005, 0.00125, 0.99, 0.985])
        # self.axes.imshow(self.data, interpolation="quadric", aspect='auto')

        # self.pnl = wx.Panel(self, wx.TOP, size=(1340, 30))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        # self.sizer.Add(self.pnl, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        cxpress = []
        cypress = []

        txpress = []
        typress = []

        def Onchange(event):

            if '-' in settings.chosen:

                cxpress.append(event.x)
                cypress.append(event.y)
                print('cxpress = ', cxpress)
                print('cypress = ', cypress)

                settings.cxpress = cxpress
                settings.cypress = cypress

            else:
                if settings.chosen:
                    txpress.append(event.x)
                    typress.append(event.y)
                    print('txpress = ', txpress)
                    print('typress = ', typress)
                    settings.txpress = txpress
                    settings.typress = typress

            '''
            xf = [settings.txpress[0], settings.txrelease[-1]]
            yf = [settings.typress[0], settings.tyrelease[-1]]
            self.axes.plot(xf, yf, color='k', linewidth=0.8)
            '''
            # settings.chosen = ''

            print('buttonbigin=%d, xbigin=%d, ybingin=%d, xdatas=%f, ydatas=%f' % (
                event.button, event.x, event.y, event.xdata, event.ydata))

            """查询按钮"""
            choice = self.FindWindowByName('gchoice')
            tname = self.FindWindowByName('tname')

            choice_test = settings.lname
            tname_test = settings.tname

            capa = self.FindWindowByName('capacity')
            capa_test = settings.capacity

            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()

            try:
                sqe = "select  polepath, tcapacity from transz where tname ='" + str(
                    tname_test) + "'and lname = '" + str(
                    choice_test) + "'"
                cue.execute(sqe)
                fpole = cue.fetchone()
                print('fpole=', fpole)
                npole = output_polepath(fpole[0])
                print('npole=', npole)
                ntcapacity = fpole[1]
                print('ntcapacity=', ntcapacity)
                cone.commit()
                cone.close()

                nipole = self.FindWindowByName('pole')
                nipole.SetValue(npole)

                nicapacity = self.FindWindowByName('capacity')
                nicapacity.SetValue(ntcapacity)
                # ntcapacity = ''
                # nicapacity.SetValue(capa_test)

                fchoice2 = self.FindWindowByName('choice2')
                fchoice2.SetValue(settings.lname + '  ' + settings.tname)

                tname.SetValue(tname_test)

                settings.capacity = ntcapacity
                settings.tname = tname_test
                settings.pole = npole
            except:

                '''
                msg3 = "无此线路或配变!"
                dialog = wx.MessageDialog(self, msg3, "提示!")
                dialog.ShowModal()  # 显示对话框
                dialog.Destroy()  # 销毁对话框
                '''
                pass

            return event.x, event.y

        # -----------------单线图--------------------
        choice = self.FindWindowByName('gchoice')

        choice_test = format(choice.GetValue())
        lname = choice_test

        transz_all = []
        cond = sqlite3.connect("fault.db3")
        cud = cond.cursor()

        polepath = []
        tcapa = []
        tname = []
        tnumber = []
        line_name = []

        pole_last = []
        tcapa_last = []
        tname_last = []
        tnumber_last = []
        line_name_last = []

        polemax = []

        sqm = "select  * from transz where lname='" + str(lname) + "'"

        cud.execute(sqm)
        total = cud.fetchall()

        polebase = 50


        kx = 1.5
        # kx = 2.5
        ky = 1.2

        for j in range(len(total)):
            # if float(total[j][5].split('-')[-1]) > 10: or total[i][1] == 'Virtual'
            # if float(total[j][5].split('-')[-1]) > 9:
            if float(total[j][5].split('-')[-1]) > 9 or total[j][1].split('.')[0] == 'Virtual':
                polemax_str = total[j][23]
                pole_str1 = polemax_str.split('.')
                print('pole_str1=', pole_str1)

                pole_num = float((pole_str1[0].split('&')[-1]).split('^')[0])
                # pole_num = float((pole_str1[0].split('&')[-1]).split('^')[0])
                polemax.append(pole_num)
                print('polemax=', polemax)
                # polebase = int(0.618 * np.max(polemax))/0.618
                polebase = int(0.618 * np.max(polemax))
                # polebase = int(1.0 * np.max(polemax))

                print('polebase=', polebase)

        # '''
        for i in range(len(total)):
            # if float(total[i][5].split('-')[-1]) > 10:
            if float(total[i][5].split('-')[-1]) > 9 or total[i][1].split('.')[0] == 'Virtual':
                pole_str = total[i][23]
                pole_str1 = pole_str.split('.')
                pole_num = float((pole_str1[0].split('&')[-1]).split('^')[0])

                # if float(total[i][9].split('.'))[1] < 50:
                if pole_num < polebase:
                    line_name.append(total[i][6])
                    polepath.append('0.' + total[i][23])
                    tcapa.append(total[i][5])
                    tname.append(total[i][3])
                    tnumber.append(total[i][4])
                else:
                    line_name_last.append(total[i][6])
                    pole_last.append('0.' + total[i][23])
                    tcapa_last.append(total[i][5])
                    tname_last.append(total[i][3])
                    tnumber_last.append(total[i][4])

        print('---------------------------------------')
        print('\n')
        print('line_name=', line_name)
        print('polepath=', polepath)

        print('\n')
        print('pole_last=', pole_last)

        print('---------------------------------------')
        print('\n')

        polepath0 = '0.17.9.4.2'
        polepath2 = '0.21.5.3.1'
        polepath3 = '0.3.26.2.2'
        polepath4 = '0.2'

        def odd(n):
            bn = n
            # bn = random.randint(0, 2)
            # print('bn=', bn)
            if bn % 2 == 1:
                return 1
            else:
                return -1

        # ---------------------------交换坐标函数------------
        # sstr 源杆号地址， ostr, 目标地址
        '''
        
        def exchange(sstr, ostr):
            # older = '7.21.3.1'
            # newer = '7.15.6'

            # older1 = sstr.split('.')
            # newer1 = ostr.split('.')

            older0 = sstr.split('.')
            newer0 = ostr.split('.')

            older1 = []
            newer1 = []

            for i in range(len(older0)):
                older1.append(older0[i].split('^')[0])

            for j in range(len(newer0)):
                newer1.append(newer0[j].split('^')[0])

            for t in range(abs(len(older1) - len(newer1))):
                if len(older1) > len(newer1):
                    newer1.append('')
                else:
                    older1.append('')

            print('older2=', older1)
            print('newer2=', newer1)

            gausess = []

            # for i in range(min(len(older1),len(newer1))):
            for i in range(min(len(older1), len(newer1))):
                gausess.append(older1[i].replace(newer1[i], ''))

            gae = []

            for j in range(len(gausess)):
                if gausess[j]:
                    gae.append(gausess[j])
                else:
                    continue

            # gau = '.'.join(gausess)

            gau3 = '.'.join(gae)

            print('gausess =', gausess)

            print('gau =', gau3)

            gau = '(' + gau3 + ')'

            return gau3
        '''


        # -----------------new function------------------------

        def exchange(sstr, ostr):
            # older = '7.21.3.1'
            # newer = '7.15.6'

            # older1 = sstr.split('.')
            # newer1 = ostr.split('.')

            older0 = sstr.split('.')
            newer0 = ostr.split('.')

            older1 = []
            newer1 = []

            for i in range(len(older0)):
                older1.append(older0[i].split('^')[0])

            for j in range(len(newer0)):
                newer1.append(newer0[j].split('^')[0])

            for t in range(abs(len(older1) - len(newer1))):
                if len(older1) > len(newer1):
                    newer1.append('')
                else:
                    older1.append('')

            print('older0=', older0)
            print('newer0=', newer0)

            print('older1=', older1)
            print('newer1=', newer1)

            print('older2=', older1)
            print('newer2=', newer1)

            gausess = []

            # for i in range(min(len(older1),len(newer1))):

            for i in range(min(len(older1), len(newer1))):
                gausess.append(older1[i].replace(newer1[i], ''))

            gae = []

            for j in range(len(gausess)):
                if gausess[j]:
                    gae.append(gausess[j])
                else:
                    continue

            # gau = '.'.join(gausess)

            gau3 = '.'.join(gae)

            if not gau3 and older1 != newer1 and older1[0] == newer1[0]:
                gau3 = older1[0]

            '''
            if not gau3 and older1[0] == newer1[0]:
                gau3 = older1[0]
            '''
            print('gausess =', gausess)

            print('gau =', gau3)

            gau = '(' + gau3 + ')'

            return gau3


        # ------------------------交换坐标函数结束--------------

        def show_map(pole_path, tcapacity, trname, trnumber):

            # -----------------------------
            choice = self.FindWindowByName('gchoice')

            choice_test = format(choice.GetValue())
            lname = choice_test

            # 通过pole_path找到正确的杆号标注
            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            # sqe = "select  polepath from transz where tnumber ='" + str(trnumber) + "'"
            sqe = "select  polepath, brancher from transz where tnumber ='" + str(trnumber) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)

            z_path0 = ('0.' + fpole[0]).split('.')
            print('z_path0=', z_path0)

            z_paths0 = fpole[0]
            z_pathw0 = fpole[1]

            if fpole[1] and fpole[1] != fpole[0]:
                z_pathraw = ('0.' + fpole[1]).split('.')
                print('z_pathraw=', z_pathraw)
            else:
                z_pathraw = ('0.' + '').split('.')
            cone.commit()
            cone.close()

            pth = pole_path
            z_path = pth.split('.')
            t_capacity = tcapacity
            t_name = trname

            z = []
            x = [0.0]
            y = [0.0]

            direction = []
            print('z_path=', z_path)

            dx = 1.0
            dxs = 1
            for k in range(len(z_path)):
                print('z_path[j]=', z_path[k])
                # if float(z_path[k]) > 50:
                # z.append(float(z_path[k]))

                z.append(float((z_path[k].split('&')[-1]).split('^')[0]))

                if '^' in z_path[k]:

                    dx = odd(int((z_path[k].split('&')[-1]).split('^')[-1]))
                    dxs = int((z_path[k].split('&')[-1]).split('^')[-1])
                    # direction.append(odd(float((z_path[k].split('&')[-1]).split('^')[-1])))
                    direction.append(odd(int((z_path[k].split('&')[-1]).split('^')[-1])))

                else:

                    direction.append(1)

                print('direction=', direction)

            print('z=', z)

            # x[0] = 0.0
            # y[0] = 0.0

            # 偶书级支线x加坐标,y不变，奇数级支线y加坐标，x不变，
            for t in range(len(z)):
                # if dxs > 2:
                # if t > 2:
                if t > 2 and dxs >= 1:

                    x[t] = x[t] + 1.0 * direction[t - 1] * (z[t] * (t % 2)) / (0.5 * t + kx)


                    # x[t] = x[t] + 1.0 * direction[t - 1] * (z[t] * (t % 2))
                    # z_path[-2] = z_path[-2].replace(z_path[-2], '0')
                else:
                    x[t] = x[t] + 1.0 * direction[t - 1] * (z[t] * (t % 2))

                # 原有算法
                # y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2))
                # kx = 0.2
                if t > 3:
                    y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2)) / (0.618 * t + kx)

                    # y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2)) / (0.867 * t + kx)

                else:
                    y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2))

                x.append(x[t])
                y.append(y[t])

            print('x=', x)
            print('y=', y)

            print('tcapacity=', t_capacity)

            self.axes.plot(x, y, color='black', linewidth=0.8)

            self.axes.scatter(0, 0, color='r', marker=align_marker('s', valign='top'), edgecolors='r', s=660,
                              linewidth=0.2)
            self.axes.scatter(0, 0, color='r', marker=align_marker('s', valign='bottom'), edgecolors='r', s=660,
                              linewidth=0.2)

            # 根据类型进行绘制原件

            print('t_capacity=', t_capacity)

            # plt.text(96, 0.04, '\n'.join(str1))   align_marker('s', valign='bottom'),

            if ('S' in t_capacity or 's' in t_capacity) and float(t_capacity.split('-')[-1]) > 9:

                self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b',
                                  s=55, linewidth=0.5, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

            else:

                if ('B' in t_capacity or 'b' in t_capacity):
                    if odd(len(z_path0)) == -1:

                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', halign='left'),
                                          edgecolors='r',
                                          s=220, linewidth=0.5)
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', halign='right'),
                                          edgecolors='r',
                                          s=220, linewidth=0.5)
                    else:
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', valign='top'),
                                          edgecolors='r',
                                          s=220,
                                          linewidth=0.5)
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', valign='bottom'),
                                          edgecolors='r',
                                          s=220,
                                          linewidth=0.5)

                # t_capacity = ''

            '''
                    self.axes.scatter(x[-1], y[-1], color='r', marker='s', edgecolors='b',
                                    s=55, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
            '''

            '''
            pick_event
            self.axes.annotate('$\circ$', xy=(x[-2], y[-2]), size=45, xytext=(-20, -25), textcoords='offset pixels')
            
            ax.annotate('pixel offset from axes fraction',
                        xy=(1, 0), xycoords='axes fraction',
                        xytext=(-20, 20), textcoords='offset pixels',
                        horizontalalignment='right',
                        verticalalignment='bottom')
            '''

            for w in range(0, len(z_path0)):
                if '^' not in z_path0[w]:
                    '''
                    self.axes.annotate("%s" % z_path0[w].replace('&', ''), xy=(x[w], y[w]), size=10,  xytext=(-10, 3), textcoords='offset points')
                                        '''

                if '^' in z_path0[w] and float(z_path0[w].replace('&', '').split('^')[-1]) > 2:
                    self.axes.annotate("%s" % z_path0[w].replace('&', '').split('^')[0].replace('Y', ''),
                                       xy=(x[w], y[w]),
                                       size=10, xytext=(-12, 3), textcoords='offset points', picker=True)

                    # pass


                else:

                    if (z_path0[w].replace('&', '').split('^')[0])[0] != '0':
                        if len((z_path0[w].replace('&', '').split('^')[0])) > 2:

                            self.axes.annotate("%s" % z_path0[w].replace('&', '').split('^')[0].replace('Y', ''),
                                               xy=(x[w], y[w]),
                                               size=10, xytext=(-18, 3), textcoords='offset points', picker=True)
                        else:
                            self.axes.annotate("%s" % z_path0[w].replace('&', '').split('^')[0].replace('Y', ''),
                                               xy=(x[w], y[w]),
                                               size=10, xytext=(-12, 3), textcoords='offset points', picker=True)

                    else:
                        self.axes.annotate('', xy=(x[w], y[w]), size=10, xytext=(-12, 3),
                                           textcoords='offset points', picker=True)

            checkpole = self.FindWindowByName('checkpole')

            checkpole_st = format(checkpole.GetValue())

            print('checkpole_st=', checkpole_st)

            print('settings.checkpole=',settings.checkpole)

            if settings.checkpole:

                lz_pathw0 = len(z_pathw0.split('.'))
                lz_pathraw = len(z_paths0.split('.'))
                deltazpath = abs(lz_pathw0 - lz_pathraw)
                # deltazpath =0

                if exchange(z_pathw0, z_paths0) and deltazpath == 0:
                    print('z_pathrawkkkkkkkkk=', z_pathraw)
                    zzpath = exchange(z_pathw0, z_paths0).split('.')

                    print('zzpath66666=', zzpath)
                    print('xx66666=', x)
                    print('exchange(z_pathw0, z_paths0)=', exchange(z_pathw0, z_paths0))
                    for g in range(-1, -len(zzpath) - 1, -1):
                        # self.axes.annotate('(' + exchange(z_pathw0, z_paths0).replace('&', '').split('^')[0].replace('Y', '') + ')', xy=(x[-len(z_pathraw)], y[-len(z_pathraw)]), size=10, xytext=(5, 3),
                        # alpha=0.5, textcoords='offset points', picker=True)


                        ck11 = self.axes.annotate(
                            '(' + zzpath[g].replace('&', '').split('^')[0].replace('Y', '') + ')',
                            xy=(x[g - 1], y[g - 1]), size=10, xytext=(5, -1 * 2 * (g - 1)),
                            alpha=0.5, textcoords='offset points', picker=True)



                        ck11.draggable()
                else:
                    if exchange(z_pathw0, z_paths0):
                        z_pathwb0 = z_pathw0.split('.')
                        z_path_all = []
                        for p in range(len(z_pathwb0)):
                            zpa = z_pathwb0[p].replace('&', '').split('^')[0].replace('Y', '')
                            z_path_all.append(zpa)

                        gaup = '.'.join(z_path_all)


                        ck12 = self.axes.annotate(
                            '(' + gaup + ')',
                            xy=(x[-2], y[-2]), size=10, xytext=(5, -3),
                            alpha=0.5, textcoords='offset points', picker=True)

                        # F&6^2.X&1
                        '''
                        ck12 = self.axes.annotate(
                            '(' + z_pathw0.replace('&', '').split('^')[0].replace('Y', '') + ')',
                            xy=(x[-2], y[-2]), size=10, xytext=(5, -3),
                            alpha=0.5, textcoords='offset points', picker=True)
                        '''



                        ck12.draggable()
            else:
                pass


            # -----------------------坐标显示start--------------------------
            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            sqe = "select  xtransformer, ytransformer, xcapacity, ycapacity from transz where tname ='" + str(
                t_name) + "' and lname='" + str(lname) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)

            cone.commit()
            cone.close()

            xtrans = fpole[0]
            ytrans = fpole[1]
            xcapas = fpole[2]
            ycapas = fpole[3]

            ztrans = math.sqrt(xtrans ** 2 + ytrans ** 2)
            zcapas = math.sqrt(xcapas ** 2 + ycapas ** 2)

            if 'T' in t_capacity or 't' in t_capacity:

                if odd(len(z_path0)) == -1:
                    if ztrans > 0.01:
                        an7 = self.axes.annotate("%s" % '\n'.join(t_name), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans - 30, ytrans - 10), color='m', verticalalignment='top',
                                                 textcoords='offset points', picker=True)
                    else:
                        an7 = self.axes.annotate("%s" % '\n'.join(t_name), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(-30, -10), color='m', verticalalignment='top',
                                                 textcoords='offset points', picker=True)
                else:
                    if ztrans > 0.01:
                        an7 = self.axes.annotate("%s" % t_name, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans + 15), color='m',
                                                 horizontalalignment='left',
                                                 textcoords='offset points', picker=True)
                    else:

                        an7 = self.axes.annotate("%s" % t_name, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, 15), color='m', horizontalalignment='left',
                                                 textcoords='offset points', picker=True)

            else:
                an7 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                         xytext=(5, 15), color='m', horizontalalignment='left',
                                         textcoords='offset points', picker=True)


            if float(t_capacity.split('-')[-1]) > 9:
                if zcapas > 0.01:

                    an9 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                             xytext=(xcapas + 5, ycapas - 15),
                                             textcoords='offset points', alpha=0.0, picker=True)

                    if 'S' in t_capacity or 's' in t_capacity:
                        an1 = self.axes.annotate("%s" % t_capacity, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                 textcoords='offset points')
                    else:
                        if 'B' in t_capacity or 'b' in t_capacity:

                            an101 = self.axes.annotate("%s" % t_capacity.split('-')[-1], xy=(x[-2], y[-2]), size=10,
                                                       xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                       textcoords='offset points')

                            an1 = self.axes.annotate("%s" % t_capacity, xy=(x[-2], y[-2]), size=10,
                                                     xytext=(xcapas + 5, ycapas - 15), alpha=0.0, picker=True,
                                                     textcoords='offset points')

                            an101.draggable()


                        else:
                            an1 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                     xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                     textcoords='offset points')


                else:

                    an9 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                             xytext=(5, -15),
                                             textcoords='offset points', alpha=0.0, picker=True)

                    if 'S' in t_capacity or 's' in t_capacity:
                        an1 = self.axes.annotate("%s" % t_capacity, xy=(x[-2], y[-2]), size=10, xytext=(5, -15),
                                                 textcoords='offset points', picker=True)
                    else:
                        if 'B' in t_capacity or 'b' in t_capacity:
                            an101 = self.axes.annotate("%s" % t_capacity.split('-')[-1], xy=(x[-2], y[-2]), size=10,
                                                       xytext=(5, -15),
                                                       textcoords='offset points', picker=True)

                            an1 = self.axes.annotate("%s" % t_capacity, xy=(x[-2], y[-2]), size=10,
                                                     xytext=(5, -15),
                                                     textcoords='offset points', alpha=0.0, picker=True)

                            an101.draggable()


                        else:
                            an1 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10, xytext=(5, -15),
                                                     textcoords='offset points', picker=True)

                if ztrans > 0.01:
                    if 'S' in t_capacity or 's' in t_capacity or 'B' in t_capacity or 'b' in t_capacity:

                        an2 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans - 30),
                                                 textcoords='offset points', picker=True)
                    else:
                        an2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans - 30),
                                                 textcoords='offset points', picker=True)
                else:
                    if 'S' in t_capacity or 's' in t_capacity or 'B' in t_capacity or 'b' in t_capacity:
                        an2 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, -30),
                                                 textcoords='offset points', picker=True)
                    else:
                        an2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, -30),
                                                 textcoords='offset points', picker=True)
                an1.draggable()
                an2.draggable()
                an7.draggable()
                an9.draggable()
                # ---------------------------------------------------------------------------------



            # cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
            # cid = self.figure.canvas.mpl_connect('button_press_event', onclick)
            cod = self.figure.canvas.mpl_connect('button_release_event', anclick)
            ced = self.figure.canvas.mpl_connect('pick_event', onpicktext)
            cud = self.figure.canvas.mpl_connect('button_press_event', Onchange)

            # ----------显示未接配变的分支箱/环网柜等Start---------------------------

            if ztrans > 0.01:
                if ('V' in t_capacity or 'v' in t_capacity) and not settings.checkpole:

                    anv2 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=8,
                                              xytext=(xtrans + 5, ytrans - 30),
                                              alpha=0.3, textcoords='offset points', picker=True)
                else:
                    anv2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=8,
                                              xytext=(xtrans + 5, ytrans - 30),
                                              alpha=0.3, textcoords='offset points', picker=True)
            else:
                if ('V' in t_capacity or 'v' in t_capacity) and not settings.checkpole:
                    anv2 = self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=8,
                                              xytext=(5, -30),
                                              alpha=0.3, textcoords='offset points', picker=True)
                else:
                    anv2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=8,
                                              xytext=(5, -30),
                                              alpha=0.3, textcoords='offset points', picker=True)

            anv2.draggable()

            # ----------显示未接配变的分支箱/环网柜等End---------------------------


            if t_name == settings.tname and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                an37 = self.axes.annotate("%s" % settings.ltname, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                an37.draggable()

            # --------------------金属故障
            if t_name == settings.atname1 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                an47 = self.axes.annotate("%s" % settings.latname1, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15),
                                          textcoords='offset points', color='#ff8000', alpha=1.0, picker=True)
                an47.draggable()

            # --------------------弧光故障
            if t_name == settings.mtname2 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                an57 = self.axes.annotate("%s" % settings.lmtname2, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                an57.draggable()

            if t_name == settings.atname2 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                an67 = self.axes.annotate("%s" % settings.latname2, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15),
                                          textcoords='offset points', color='#ff8000', alpha=1.0, picker=True)
                an67.draggable()

            # --------------------主线故障
            if t_name == settings.mtname3 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                cn57 = self.axes.annotate("%s" % settings.lmtname3, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                cn57.draggable()

            if t_name == settings.atname3 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                cn67 = self.axes.annotate("%s" % settings.latname3, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15),
                                          textcoords='offset points', color='#ff8000', alpha=1.0, picker=True)
                cn67.draggable()

            # -------------------

            # wi.plot_text("%s" % t_name.replace('&', ''), x[-2], y[-2])
            # wi.plot(x, y, color='black', linewidth=0.8)
            # lmtname2 = ''         latname2 = ''

            '''
            for t in range(0, len(z_path0)):
                if ('F' in z_path0[t] or 'f' in z_path0[t]):
                    self.axes.scatter(x[t], y[t], color='k', marker='s', edgecolors='k',
                                      s=110, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                if ('H' in z_path0[t] or 'h' in z_path0[t]):
                    self.axes.scatter(x[t], y[t], color='k', marker='s', edgecolors='k',
                                      s=110, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                if ('X' in z_path0[t] or 'x' in z_path0[t]):
                    self.axes.scatter(x[t], y[t], color='k', marker='s', edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
            '''
            return x, y

        def show_last(zbase, pole_last, cpacity_last, trname_last, trnumber_last):

            choice = self.FindWindowByName('gchoice')

            choice_test = format(choice.GetValue())
            lname = choice_test

            # 通过pole_path找到正确的杆号标注
            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            sqe = "select  polepath, brancher  from transz where  tnumber ='" + str(trnumber_last) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            z_path9 = ('0.' + fpole[0]).split('.')
            print('z_path0=', z_path9)

            z_pathw0 = fpole[1]
            z_paths0 = fpole[0]

            if fpole[1] and fpole[1] != fpole[0]:
                z_pathraw = ('0.' + fpole[1]).split('.')
                print('z_pathraw=', z_pathraw)
            else:
                z_pathraw = ('0.' + '').split('.')

            cone.commit()
            cone.close()

            z_base = zbase
            capa_last = cpacity_last
            tname_last = trname_last

            print('\n')
            print('capa_last=', capa_last)
            print('tname_last=', trname_last)

            z_path0 = pole_last

            print('\n')
            print('z_path0=', z_path0)

            z_path = z_path0.split('.')
            print('\n')
            print('z_path=', z_path)

            z = []
            x = [z_base]
            y = [0]

            print('z_path=', z_path)

            direction = []
            print('z_path=', z_path)

            dx = 1.0
            dxs = 1
            for k in range(len(z_path)):
                print('z_path[j]=', z_path[k])
                # if float(z_path[k]) > 50:
                # z.append(float(z_path[k]))

                z.append(float((z_path[k].split('&')[-1]).split('^')[0]))

                if '^' in z_path[k]:

                    dx = odd(int((z_path[k].split('&')[-1]).split('^')[-1]))
                    dxs = int((z_path[k].split('&')[-1]).split('^')[-1])
                    # direction.append(odd(float((z_path[k].split('&')[-1]).split('^')[-1])))
                    direction.append(odd(int((z_path[k].split('&')[-1]).split('^')[-1])))

                else:

                    direction.append(1)

                print('direction=', direction)

            print('z=', z)

            '''
            for k in range(len(z_path)):
                print('z_path[j]=', z_path[k])
                z.append(float((z_path[k].split('&')[-1]).split('^')[0]))

            print('z=', z)
            '''

            # x[0] = 0.0
            # y[0] = 0.0

            # 偶数级支线x加坐标,y不变，奇数级支线y加坐标，x不变，

            for t in range(len(z)):

                if t > 1 and dxs >= 1:

                    # if t > 2:
                    y[t] = y[t] - direction[t - 1] * (z[t] * (t % 2))
                    x[t] = x[t] + direction[t - 1] * (z[t] * ((t + 1) % 2)) / (0.5 * t + kx)
                    # x[t] = x[t] - direction[t - 1] * (z[t] * ((t + 1) % 2))
                else:
                    y[t] = y[t] - direction[t - 1] * (z[t] * (t % 2))
                    # x[t] = x[t] - direction[t - 1] * (z[t] * ((t + 1) % 2))
                    x[t] = x[t] + direction[t - 1] * (z[t] * ((t + 1) % 2))

                x.append(x[t])
                y.append(y[t])

            for w in range(len(y)):
                y[w] = y[w] + z_base

            # y[:] = [y + z_base for y in y]

            y[0] = 0

            x.insert(0, 0)
            y.insert(0, 0)

            print('x=', x)
            print('y=', y)

            self.axes.plot(x, y, color='black', linewidth=0.8)
            # if ('S' in t_capacity or 's' in t_capacity) and float(t_capacity.split('-')[-1]) > 9:


            if ('S' in capa_last or 's' in capa_last) and float(capa_last.split('-')[-1]) > 9:

                self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b',
                                  s=55, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
            else:

                if ('B' in capa_last or 'b' in capa_last):

                    if odd(len(z_path9)) == 1:

                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', halign='left'),
                                          edgecolors='r',
                                          s=220, linewidth=0.5)
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', halign='right'),
                                          edgecolors='r',
                                          s=220, linewidth=0.5)
                    else:
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', valign='top'),
                                          edgecolors='r',
                                          s=220,
                                          linewidth=0.5)
                        self.axes.scatter(x[-1], y[-1], color='r', marker=align_marker('s', valign='bottom'),
                                          edgecolors='r',
                                          s=220,
                                          linewidth=0.5)

                # capa_last = ''

            # plt.annotate("%s" % z_path[-1], xy=(x[-2], y[-2]), size=10, xytext=(10, 0), textcoords='offset points')
            # 新的标注方法

            print('z_path9=', z_path9)

            for w in range(-1, -len(z_path9), -1):
                if '^' not in z_path9[w]:
                    '''
                    self.axes.annotate("%s" % z_path9[w].replace('&', ''), xy=(x[w], y[w]), size=10,  xytext=(-12, 3), textcoords='offset points')
                    '''

                if '^' in z_path9[w] and float(z_path9[w].replace('&', '').split('^')[-1]) > 2:
                    if len((z_path9[w].replace('&', '').split('^')[0])) > 2:
                        self.axes.annotate("%s" % z_path9[w].replace('&', '').split('^')[0].replace('Y', ''),
                                           xy=(x[w - 1], y[w - 1]),
                                           size=10, xytext=(-12, 3), textcoords='offset points', picker=True)
                    else:
                        self.axes.annotate("%s" % z_path9[w].replace('&', '').split('^')[0].replace('Y', ''),
                                           xy=(x[w - 1], y[w - 1]),
                                           size=10, xytext=(-12, 3), textcoords='offset points', picker=True)
                    # pass
                else:

                    if (z_path9[w].replace('&', '').split('^')[0])[0] != '0':
                        if len((z_path9[w].replace('&', '').replace('Y', '').split('^')[0])) > 2:
                            self.axes.annotate("%s" % z_path9[w].replace('&', '').split('^')[0].replace('Y', ''),
                                               xy=(x[w - 1], y[w - 1]),
                                               size=10, xytext=(-18, 3), textcoords='offset points', picker=True)
                        else:
                            self.axes.annotate("%s" % z_path9[w].replace('&', '').split('^')[0].replace('Y', ''),
                                               xy=(x[w - 1], y[w - 1]),
                                               size=10, xytext=(-12, 3), textcoords='offset points', picker=True)

                    else:
                        self.axes.annotate('', xy=(x[w], y[w]), size=10, xytext=(-18, 3),
                                           textcoords='offset points', picker=True)

            # -----------------------GOOD--------------------------

            # ---------------------GOODEND--------------------

            if settings.checkpole:

                lz_pathw0 = len(z_pathw0.split('.'))
                lz_pathraw = len(z_paths0.split('.'))
                deltazpath = abs(lz_pathw0 - lz_pathraw)

                if exchange(z_pathw0, z_paths0) and deltazpath == 0:
                    zzpath = exchange(z_pathw0, z_paths0).split('.')

                    print('zzpath66666=', zzpath)
                    print('xx66666=', x)
                    print('exchange(z_pathw0, z_paths0)=', exchange(z_pathw0, z_paths0))
                    for g in range(-1, -len(zzpath) - 1, -1):
                        # self.axes.annotate('(' + exchange(z_pathw0, z_paths0).replace('&', '').split('^')[0].replace('Y', '') + ')', xy=(x[-len(z_pathraw)], y[-len(z_pathraw)]), size=10, xytext=(5, 3),
                        # alpha=0.5, textcoords='offset points', picker=True)
                        ck21 = self.axes.annotate(
                            '(' + zzpath[g].replace('&', '').split('^')[0].replace('Y', '') + ')',
                            xy=(x[g - 1], y[g - 1]), size=10, xytext=(-25, -3 * 2 * (g - 1)),
                            alpha=0.5, textcoords='offset points', picker=True)
                        ck21.draggable()
                else:
                    if exchange(z_pathw0, z_paths0):
                        ck22 = self.axes.annotate('(' + z_pathw0.replace('&', '').replace('Y', '') + ')',
                                           xy=(x[-2], y[-2]), size=10, xytext=(-5, +12), alpha=0.5,
                                           textcoords='offset points', picker=True)
                        ck22.draggable()
            else:
                pass

            # -----------------------坐标显示start--------------------------

            # 新标注方法，全面

            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            sqe = "select  xtransformer, ytransformer, xcapacity, ycapacity from transz where tname ='" + str(
                trname_last) + "' and lname='" + str(lname) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)

            cone.commit()
            cone.close()

            xtrans = fpole[0]
            ytrans = fpole[1]
            xcapas = fpole[2]
            ycapas = fpole[3]
            ztrans = math.sqrt(xtrans ** 2 + ytrans ** 2)
            zcapas = math.sqrt(xcapas ** 2 + ycapas ** 2)

            if 'T' in capa_last or 't' in capa_last:

                if odd(len(z_path9)) == 1:
                    if ztrans > 0.01:
                        an6 = self.axes.annotate("%s" % '\n'.join(tname_last), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans - 30, ytrans - 10), color='m', verticalalignment='top',
                                                 textcoords='offset points', picker=True)
                    else:

                        an6 = self.axes.annotate("%s" % '\n'.join(tname_last), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(-30, -10), color='m', verticalalignment='top',
                                                 textcoords='offset points', picker=True)
                else:
                    if ztrans > 0.01:
                        an6 = self.axes.annotate("%s" % tname_last, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans + 15), color='m',
                                                 horizontalalignment='left',
                                                 textcoords='offset points', picker=True)
                    else:
                        an6 = self.axes.annotate("%s" % tname_last, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, 15), color='m', horizontalalignment='left',
                                                 textcoords='offset points', picker=True)
            else:
                an6 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                         xytext=(5, 15), color='m', horizontalalignment='left',
                                         textcoords='offset points', picker=True)

            if float(capa_last.split('-')[-1]) > 9:
                if zcapas > 0.01:

                    an10 = self.axes.annotate("%s" % tname_last.replace('&', ''), xy=(x[-2], y[-2]), size=10,

                                              xytext=(xcapas + 5, ycapas - 15),
                                              textcoords='offset points', alpha=0.0, picker=True)

                    if 'S' in capa_last or 's' in capa_last:
                        an3 = self.axes.annotate("%s" % capa_last, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                 textcoords='offset points')

                    else:
                        if 'B' in capa_last or 'b' in capa_last:

                            an3 = self.axes.annotate("%s" % capa_last.split('-')[-1], xy=(x[-2], y[-2]), size=10,
                                                     xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                     textcoords='offset points')

                            an301 = self.axes.annotate("%s" % capa_last, xy=(x[-2], y[-2]), size=10,
                                                       xytext=(xcapas + 5, ycapas - 15), alpha=0.0, picker=True,
                                                       textcoords='offset points')

                            an301.draggable()
                        else:
                            an3 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                     xytext=(xcapas + 5, ycapas - 15), picker=True,
                                                     textcoords='offset points')



                else:
                    an10 = self.axes.annotate("%s" % tname_last, xy=(x[-2], y[-2]), size=10, xytext=(5, -15),
                                              textcoords='offset points', alpha=0.0, picker=True)

                    if 'S' in capa_last or 's' in capa_last:
                        an3 = self.axes.annotate("%s" % capa_last, xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, -15), picker=True,
                                                 textcoords='offset points')


                    else:
                        if 'B' in capa_last or 'b' in capa_last:

                            an3 = self.axes.annotate("%s" % capa_last.split('-')[-1], xy=(x[-2], y[-2]), size=10,
                                                     xytext=(5, - 15), picker=True,
                                                     textcoords='offset points')

                            an301 = self.axes.annotate("%s" % capa_last, xy=(x[-2], y[-2]), size=10,
                                                       xytext=(5, - 15), alpha=0.0, picker=True,
                                                       textcoords='offset points')

                            an301.draggable()
                        else:
                            an3 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                     xytext=(5, -15), picker=True,
                                                     textcoords='offset points')

                if ztrans > 0.01:
                    if 'S' in capa_last or 's' in capa_last or 'B' in capa_last or 'b' in capa_last:

                        an4 = self.axes.annotate("%s" % tname_last.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans - 30),
                                                 textcoords='offset points', picker=True)

                        

                    else:
                        an4 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                 xytext=(xtrans + 5, ytrans - 30),
                                                 textcoords='offset points', picker=True)
                else:
                    if 'S' in capa_last or 's' in capa_last or 'B' in capa_last or 'b' in capa_last:
                        an4 = self.axes.annotate("%s" % tname_last.replace('&', ''), xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, -30),
                                                 textcoords='offset points', picker=True)
                    else:
                        an4 = self.axes.annotate('', xy=(x[-2], y[-2]), size=10,
                                                 xytext=(5, -30),
                                                 textcoords='offset points', picker=True)

                an10.draggable()
                an3.draggable()
                an4.draggable()
                an6.draggable()
            

            
            # zid = self.figure.canvas.mpl_connect('button_press_event', onclick)
            zod = self.figure.canvas.mpl_connect('button_release_event', anclick)
            zed = self.figure.canvas.mpl_connect('pick_event', onpicktext)
            zud = self.figure.canvas.mpl_connect('button_press_event', Onchange)

            # ----------显示未接配变的分支箱/环网柜等Start---------------------------

            if ztrans > 0.01:
                if ('V' in capa_last or 'v' in capa_last) and not settings.checkpole:

                    anv2 = self.axes.annotate("%s" % tname_last.replace('&', ''), xy=(x[-2], y[-2]), size=8,
                                              xytext=(xtrans + 5, ytrans - 30),
                                              alpha=0.3, textcoords='offset points', picker=True)
                else:
                    anv2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=8,
                                              xytext=(xtrans + 5, ytrans - 30),
                                              alpha=0.3, textcoords='offset points', picker=True)
            else:
                if ('V' in capa_last or 'v' in capa_last) and not settings.checkpole:
                    anv2 = self.axes.annotate("%s" % tname_last.replace('&', ''), xy=(x[-2], y[-2]), size=8,
                                              xytext=(5, -30),
                                              alpha=0.3, textcoords='offset points', picker=True)
                else:
                    anv2 = self.axes.annotate('', xy=(x[-2], y[-2]), size=8,
                                              xytext=(5, -30),
                                              alpha=0.3, textcoords='offset points', picker=True)

            anv2.draggable()

            # ----------显示未接配变的分支箱/环网柜等End---------------------------


            # wi.plot(x, y, color='black', linewidth=0.8)
            ##

            # self.axes.plot(x, y, color='black', linewidth=0.8)

            # plt.plot(x, y, color='black', linewidth=0.8)
            # self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b', s=55)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
            # self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b', s=55)

            print('settings.ltname=', settings.ltname)
            print('settings.latname1=', settings.latname1)
            if tname_last == settings.tname and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                an17 = self.axes.annotate("%s" % settings.ltname, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                an17.draggable()
            # settings.ltname

            if tname_last == settings.atname1 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                an27 = self.axes.annotate("%s" % settings.latname1, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15), textcoords='offset points', color='#ff8000', alpha=1.0,
                                          picker=True)
                an27.draggable()

            # --------------------
            if tname_last == settings.mtname2 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                an87 = self.axes.annotate("%s" % settings.lmtname2, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                an87.draggable()

            if tname_last == settings.atname2 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                an97 = self.axes.annotate("%s" % settings.latname2, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15),
                                          textcoords='offset points', color='#ff8000', alpha=1.0, picker=True)
                an97.draggable()

            # --------------------主线故障
            if tname_last == settings.mtname3 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='g',
                                  s=660, linewidth=2.5)
                cn57 = self.axes.annotate("%s" % settings.lmtname3, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +25),
                                          textcoords='offset points', color='g', alpha=1.0, picker=True)
                cn57.draggable()

            if tname_last == settings.atname3 and lname == settings.lname:
                self.axes.scatter(x[-1], y[-1], color='', marker='o', edgecolors='#ff8000',
                                  s=440, linewidth=2.5)
                cn67 = self.axes.annotate("%s" % settings.latname3, xy=(x[-1], y[-1]), size=10,
                                          xytext=(-40, +15),
                                          textcoords='offset points', color='#ff8000', alpha=1.0, picker=True)
                cn67.draggable()

            # -------------------

            return x, y

        # print('3^2=', '3^2'.split('^'))

        tbsxy = []
        tbexy = []

        xnmax = [0.0]
        ynmax = [0.0]

        xnmin = [0.0]
        ynmin = [0.0]

        for j in range(len(polepath)):
            print('\n')
            print('polepath[j]=', polepath[j])
            xn, yn = show_map(polepath[j], tcapa[j], tname[j], tnumber[j])
            print('xn=', xn)
            tbsxy.append([tname[j], tcapa[j], xn, yn])

            z_path0 = (polepath[j]).split('.')
            print('z_path0x=', z_path0)

            for t in range(0, len(z_path0)):
                if ('F' in z_path0[t] or 'f' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('G' in z_path0[t] or 'g' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('H' in z_path0[t] or 'h' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                if ('L' in z_path0[t] or 'l' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('X' in z_path0[t] or 'x' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='b', marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('Z' in z_path0[t] or 'z' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='y', marker=MarkerStyle('s', fillstyle='bottom'),
                                      edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    self.axes.scatter(xn[t], yn[t], color='w', marker=MarkerStyle('s', fillstyle='top'), edgecolors='k',
                                      s=85, linewidth=0.5, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    '''
                    self.axes.annotate('$\circ$', xy=(xn[t], yn[t]), size=42, xytext=(-2, -8),
                                       textcoords='offset points', horizontalalignment='center',
                                       verticalalignment='center')
                    '''

                if ('Y' in z_path0[t] or 'y' in z_path0[t]):
                    self.axes.scatter(xn[t], yn[t], color='y', marker=MarkerStyle('o', fillstyle='bottom'),
                                      edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    self.axes.scatter(xn[t], yn[t], color='w', marker=MarkerStyle('o', fillstyle='top'), edgecolors='k',
                                      s=85, linewidths=0.5, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                    '''
                    self.axes.annotate('$\circ$', xy=(xn[t], yn[t]), size=32.5, xytext=(0, 0),
                                       textcoords='offset pixels', horizontalalignment='center',
                                       verticalalignment='top')
                    self.axes.annotate('$\circ$', xy=(xn[t], yn[t]), size=32.5, xytext=(0, -6.5),
                                       textcoords='offset pixels', horizontalalignment='center',
                                       verticalalignment='top')
                    '''
            '''
            self.axes.annotate('$\circ$', xy=(x[-2], y[-2]), size=45, xytext=(-20, -25), textcoords='offset pixels')
            
            ax.annotate('pixel offset from axes fraction',
                        xy=(1, 0), xycoords='axes fraction',
                        xytext=(-20, 20), textcoords='offset pixels',
                        horizontalalignment='right',
                        verticalalignment='bottom')
            '''

            xnmax.append(xn)
            ynmax.append(max(yn))
            print('xn=', xn)

            xnmin.append(min(xn))
            ynmin.append(min(yn))

        xmmax = [0.0]
        ymmax = [0.0]

        xmmin = [0.0]
        ymmin = [0.0]

        zmin = [0.0]
        zlins = [0.0]

        # zlins0 = float(pole_last[0].split('.')[1].split('^')[0].split('&')[-1])

        print('pole_last=', pole_last)

        print('pole_last[0]=', pole_last[0])

        zlins = abs(int(pole_last[0].split('.')[1].split('^')[0].split('&')[-1]))

        # for j in range(1, len(pole_last)):
        for j in range(0, len(pole_last)):

            print('\n')
            print('pole_last[j]=', pole_last[j])
            xm, ym = show_last(polebase, pole_last[j], tcapa_last[j], tname_last[j], tnumber_last[j])
            tbsxy.append([tname_last[j], tcapa_last[j], xm, ym])

            z_path9 = (pole_last[j]).split('.')
            print('z_path9x=', z_path9)
            for t in range(len(z_path9)):
                if ('F' in z_path9[t] or 'f' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                if ('G' in z_path9[t] or 'g' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('H' in z_path9[t] or 'h' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                if ('L' in z_path9[t] or 'l' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='b', alpha=1.0, marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('X' in z_path9[t] or 'x' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='b', marker='s', edgecolors='b',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

                if ('Z' in z_path9[t] or 'z' in z_path9[t]):
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='y', marker=MarkerStyle('s', fillstyle='bottom'),
                                      edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='w', marker=MarkerStyle('s', fillstyle='top'),
                                      edgecolors='k',
                                      s=85, linewidth=0.5, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）



                if ('Y' in z_path9[t] or 'y' in z_path9[t]):
                    '''
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='w', marker='s', edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    '''
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='y', marker=MarkerStyle('o', fillstyle='bottom'),
                                      edgecolors='k',
                                      s=85, picker=True, pickradius=5)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
                    self.axes.scatter(xm[t + 1], ym[t + 1], color='w', marker=MarkerStyle('o', fillstyle='top'),
                                      edgecolors='k',
                                      s=85, linewidth=0.5, picker=True, pickradius=5)



            xmmax.append(xm)
            ymmax.append(max(ym))

            xmmin.append(min(xm))
            ymmin.append(min(ym))

            print('pole_last[(?)]=(?)', j, pole_last[j])

            if abs(int(pole_last[j].split('.')[1].split('^')[0].split('&')[-1])) > abs(int(zlins)):
                zmin.append(min(ym))
                zlins = abs(float(pole_last[j].split('.')[1].split('^')[0].split('&')[-1]))
            else:
                zlins = zlins

        print('tbsxy=', tbsxy)
        print('ymmax=', ymmax)
        print('zmin=', zmin)

        self.axes.plot([0.0, int(polebase)], [0.0, 0.0], color='red')
        # self.axes.plot([int(polebase), int(polebase)], [0.0, zmin[-1]], color='red')
        self.axes.plot([int(polebase), int(polebase)], [0.0, min(zmin)], color='red')

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()
        sqe = "select  company, station from line where lname ='" + str(lname) + "'"
        cue.execute(sqe)
        ftotal = cue.fetchone()
        print('ftotal=', ftotal)
        fcompany = ftotal[0]
        fstation = ftotal[1]

        cone.commit()
        cone.close()

        '''
        bn22 = self.axes.annotate("%s" % '10kV' + lname, xy=(0, 0), size=10, xytext=(10, 15),
                                  textcoords='offset points')
        
        bn22.draggable()
        '''

        bn2 = self.axes.annotate("%s" % '' + fstation, xy=(0, 0), size=10, xytext=(-30, 20),
                                 textcoords='offset points')

        bn2.draggable()

        '''
        sqe = "select  xtransformer, ytransformer, xcapacity, ycapacity from transz where tname ='" + str(
            trname_last) + "' and lname='" + str(lname) + "'"
        ORDER BY SALARY ASC
        
        SELECT price FROM fruitforsale WHERE fruit='Orange' ORDER BY state;
        '''
        print('lname=', lname)
        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()
        # sqe = "select  id, tnumber from transz order by id ASC where  lname ='" + str(lname) + "'"
        sqe = "SELECT  id, lname, tname, tnumber  FROM   transz    where  lname ='" + str(
            lname) + "'" + "ORDER BY id desc"

        cue.execute(sqe)
        fnumber = cue.fetchall()
        chosenumber = fnumber[0][3]
        print('fnumber=', fnumber)
        print('chosenumber=', chosenumber)
        cone.commit()
        cone.close()

        # 获取主变台数和容量Start

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()
        # sqe = "select  id, tnumber from transz order by id ASC where  lname ='" + str(lname) + "'"
        sqe = "SELECT  lname, tcapacity FROM   transz    where  lname ='" + str(
            lname) + "'" + "ORDER BY id desc"

        cue.execute(sqe)
        fcapacity = cue.fetchall()
        chosecapacity = fcapacity[0][1]
        print('fcapacity=', fcapacity)
        print('chosecapacity=', chosecapacity)
        cone.commit()
        cone.close()

        capa_all = 0
        call_number = 0
        for i in range(len(fcapacity)):
            if float(fcapacity[i][1].split('-')[-1]) > 9 and 'S' in fcapacity[i][1]:
                capa_all = capa_all + int(fcapacity[i][1].split('-')[-1])
                call_number = call_number + 1
            else:
                capa_all = capa_all
                call_number = call_number
        print('capa_all=', capa_all)
        print('call_number=', call_number)

        # 获取主变台数和容量End

        choseblock = chosenumber + '.' + str(call_number) + '.' + str(capa_all)

        bn5 = self.axes.annotate("%s" % '区块号：' + choseblock,
                                 xy=(min([min(xnmin), min(xmmin)]), min([min(ynmin), min(ymmin)])), size=10, color='g',
                                 xytext=(0, 0),
                                 textcoords='offset points', wrap=True)
        bn5.draggable()

        bn22 = self.axes.annotate("%s" % '变电站：' + fstation,
                                  xy=(min([min(xnmin), min(xmmin)]), min([min(ynmin), min(ymmin)])), size=10, color='g',
                                  xytext=(0, 20), alpha=0.5, textcoords='offset points')

        bn22.draggable()

        '''
        bn33 = self.axes.annotate("%s" % '名人堂：' + settings.user,
                                  xy=(min([min(xnmin), min(xmmin)]), min([min(ynmin), min(ymmin)])), size=10, color='g',
                                  xytext=(0, 40), alpha=0.5, textcoords='offset points')

        bn33.draggable()
        '''

        self.axes.set_xticks([])
        self.axes.set_yticks([])

        # 'inputdata' + '\\' + '\\' + str(transz_name1)
        self.figure.savefig('outputdata\\svg' + '\\' + '\\' + '10kV' + lname + '.svg', dpi=600, format='svg')
        # self.figure.savefig('outputdata\\svg' + '\\' + '\\' + '10kV' + lname + '.pdf', dpi=600, format='pdf')

        # self.axes.legend(fontsize=12)
        '''
        self.axes.text(0.5, 0.5, 'Created by Luoyeanling', transform=self.axes.transAxes,
                fontsize=30, color='gray', alpha=0.5,
                ha='center', va='center', rotation='25')
        '''


        # settings.checkpole = False



def energetic(block):
    elective = block
    try:
        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()
        sql = "select * from picture where timestamp='" + elective + "'"
        cur.execute(sql)
        total = cur.fetchone()
        elastics = total[3]
        conn.commit()
        conn.close()
    except:

        piclist = ['default.jpg', 'default2.jpg', 'default3.jpg', 'default4.jpg', 'default5.jpg']
        elastics = random.sample(piclist, 1)[0]
        # elastics = random.randint(piclist)
        # elastics = 'default.jpg'

    print('timestamp=', elastics)
    return elastics


def ectopic(block, wfline):
    app2 = Flask('app2')
    # app2.config['UPLOAD_FOLDER'] = 'uploads'
    app2.config['UPLOAD_FOLDER'] = 'inputdata'
    easymock = block
    elelines = wfline
    print('eleline=', elelines)

    def genFilename(s):
        arr_s = s.split('.')
        t = time.strftime("%Y%m%d%H%M%S", time.localtime())
        return arr_s[0] + '-' + t + '.' + arr_s[1]

    def createDBTable():
        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()
        try:
            cur.execute("""
                                                    create table picture (id INT not null, 
                                                                        timestamp varchar(150), 
                                                                        line varchar(50),
                                                                        pic  varchar(150),
                                                                        picraw  varchar(150),
                                                                        picbase  BLOB,
                                                                        picinfo  varchar(150)
                                                                         ); """)
            conn.commit()
        except:
            sql = "select * from picture"
            cur.execute(sql)

            conn.commit()

        return True

    createDBTable()

    @app2.route('/uploads/<filename>')
    def uploaded_file(filename):

        return send_from_directory(app2.config['UPLOAD_FOLDER'], filename)

    @app2.route("/", methods=['GET', 'POST'])
    def home():
        elaine = settings.PRODUCTS[0]['线路名称']
        entire = settings.PRODUCTS[0]['时间']
        picinfomation = settings.PRODUCTS[0]['故障信息']
        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()
        sql = "select * from picture"
        cur.execute(sql)
        total = len(cur.fetchall()) + 1

        conn.commit()
        print('elaine=', elaine)
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            file = request.files['file']
            filename_raw = file.filename
            file.filename = genFilename(file.filename)
            # Generate new filename
            # file.filename2 = line + '-' + faultblock + '.jpg'
            # file.filename2 = elaine + '-' + file.filename
            # file.filename2 = settings.lname + '-' + file.filename
            # 2021-06-08
            file.filename2 = file.filename

            print('file.filename=', file.filename)
            print('file.filename2=', file.filename2)

            if file:
                # Save file to server
                file.save(os.path.join(app2.config['UPLOAD_FOLDER'], file.filename2))
                # file.save(os.path.join(app2.config['UPLOAD_FOLDER'], file.filename))
            file_url = request.url + 'inputdata/' + file.filename2
            # Insert file url into the database

            # file2 = open('inputdata/' + file.filename2, 'rb')

            file2 = open(file.filename2, 'rb')

            b64 = base64.b64encode(file2.read())
            file2.close()

            # print('b64=', b64)
            '''
            conn = sqlite3.connect("fault.db3")
            cur = conn.cursor()
            cur.execute("INSERT INTO picture VALUES(?,?,?,?,?,?,?)",
                        [total, entire, elaine, (format(file.filename2)), filename_raw, (format(b64)), picinfomation])

            conn.commit()
            conn.close()
            '''

            # ------数据录入transz------
            addtransz(file.filename2)
            # ------数据录入transz------

            return 'Your pic path is:  ' + file_url
        else:
            return 'Invalid'

    print('bad')

    webbrowser.open('http://127.0.0.1:5001/')
    app2.run(host='localhost', port=5001, debug=False, threaded=True, use_reloader=False)

    return True


class WorkThread(threading.Thread):

    def __init__(self):
        """Init Worker Thread Class."""
        self.datapic2 = settings.PRODUCTS
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        pub.sendMessage("update", mstatus='eleworkstart')

        print('self.datapic2=', self.datapic2)
        print('pic')
        settings.PRODUCTS = self.datapic2
        result = ectopic(self.datapic2[0]['时间'], self.datapic2[0]['线路名称'])
        print('result=', result)

        wx.CallAfter(pub.sendMessage, "update", msg=1)
        time.sleep(0.5)


class Disframe(wx.Frame):



    def __init__(self, parent):
        # self.on_Radiot_click = None
        self.on_Radiot_click = None
        self.data = settings.PRODUCTS
        self.data2 = settings.PRODUCTSALL
        # wx.Frame.__init__(self, None, -1, '【配网自动成图】', size=(900, 760))
        holder = settings.holder
        version = settings.version
        # self.SetStatusText("Elenut All Rights Reserved. Copyright © 2020.02" + '   Version=1.1.2')

        # wx.Frame.__init__(self, None, -1, '【配网自动成图】- ' + holder + version, size=(1340, 820))

        wx.Frame.__init__(self, None, -1, '【配网自动成图】- ' + holder + version, size=(1340, 1010))

        ico = wx.Icon("resources/bats.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        # panel = wx.Panel(self, wx.Center, size=(1340, 10))

        panel = wx.Panel(self, wx.Center, size=(1340, 10))

        self.SetBackgroundColour('#f5f5d5')
        # ----------------------
        # panelsearch = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        panelsearch = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        choice2 = wx.TextCtrl(panelsearch, name="choice2", value=settings.lname + '   ' + settings.tname,
                              size=(960, 30), style=wx.TE_CENTER)

        choice2.Bind(wx.EVT_RIGHT_DOWN, self.OnEnterWindow)  # 2 绑定鼠标位于其上事件

        choice2_time = wx.TextCtrl(panelsearch, name="choice2_time", value=settings.company, size=(90, 30),
                                   style=wx.TE_CENTER)
        choice2_time.Bind(wx.EVT_RIGHT_DOWN, self.OnEnterCompany)  # 2 绑定鼠标位于其上事件

        search2_btn = wx.Button(parent=panelsearch, label="手气不错", size=wx.Size(70, 30))
        self.Bind(wx.EVT_BUTTON, self.search2_btn_onclick, search2_btn)

        search_btn = wx.Button(parent=panelsearch, label="搜索", size=wx.Size(80, 30))
        self.Bind(wx.EVT_BUTTON, self.search_btn_onclick, search_btn)
        boxsearch = wx.BoxSizer(wx.HORIZONTAL)
        boxsearch.AddSpacer(1)  # 添加空白

        boxsearch.Add(search2_btn, 1, flag=wx.ALL | wx.FIXED_MINSIZE, border=1)

        boxsearch.Add(choice2, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        boxsearch.Add(choice2_time, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        boxsearch.Add(search_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=0)

        panelsearch.SetSizer(boxsearch)
        # --------------------------------------------------------

        # panelinfo = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        panelinfo = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        picoo_btn_st = wx.StaticText(panelinfo, label="线路名称:", size=(80, 30), style=wx.TE_LEFT | wx.Center)
        picoo_btn = wx.TextCtrl(panelinfo, name="gchoice", value=settings.lname, size=(120, 30), style=wx.BU_LEFT)
        # picoo_btn = wx.TextCtrl(panelinfo, name="choice", value='南大线', size=(260, 20), style=wx.BU_LEFT)
        tname_st = wx.StaticText(panelinfo, label="设备型号:", size=(80, 30), style=wx.TE_LEFT | wx.Center)
        tname = wx.TextCtrl(panelinfo, name="capacity", value=settings.capacity, size=(120, 30), style=wx.BU_LEFT)

        picbutton = wx.Button(panelinfo, label="导入数据", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.uploadPhoto, picbutton)

        addtrans = wx.Button(panelinfo, label="新增设备", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.Andtrans, addtrans)

        modifytrans = wx.Button(panelinfo, label="更新数据", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.Modifytrans, modifytrans)

        button = wx.Button(panelinfo, label="配网成图", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.showgram, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        boxh = wx.BoxSizer(wx.HORIZONTAL)

        boxh.Add(picbutton, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=1)
        boxh.AddSpacer(15)
        boxh.Add(addtrans, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(15)
        boxh.Add(picoo_btn_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(picoo_btn, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(15)

        # -----------------
        trans_st = wx.StaticText(panelinfo, label="设备名称:", size=(80, 30), style=wx.TE_LEFT)
        trans = wx.TextCtrl(panelinfo, name="tname", value=settings.tname, size=(120, 30), style=wx.BU_LEFT)
        trans.Bind(wx.EVT_RIGHT_DOWN, self.OnEntertrans)

        pole_st = wx.StaticText(panelinfo, label="杆号路径:", size=(80, 30), style=wx.TE_LEFT)
        pole = wx.TextCtrl(panelinfo, name="pole", value=settings.pole, size=(150, 30), style=wx.BU_LEFT)

        chearray = wx.CheckBox(panelinfo, label='Original', size=(50, 30), style=wx.BU_LEFT, name="checkpole")
        chearray.SetValue(settings.checkpole)


        self.Bind(wx.EVT_CHECKBOX, self.onChecked)

        boxh.Add(trans_st, 0, flag=wx.FIXED_MINSIZE | wx.ALIGN_LEFT | wx.ALL, border=1)
        boxh.Add(trans, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(tname_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(tname, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(pole_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(pole, 1, flag=wx.EXPAND, border=1)

        boxh.AddSpacer(10)
        boxh.Add(chearray, 1, flag=wx.FIXED_MINSIZE | wx.ALIGN_LEFT | wx.ALL, border=1)

        boxh.AddSpacer(10)
        boxh.Add(button, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(modifytrans, 1, flag=wx.EXPAND, border=1)
        box_info = wx.BoxSizer(wx.VERTICAL)

        box_info.Add(boxh, 1, flag=wx.EXPAND, border=0)
        box_info.AddSpacer(10)
        # box_info.Add(boxt, 1, flag=wx.EXPAND, border=1)
        # box_info.AddSpacer(10)
        # box_info.Add(boxm, 1, flag=wx.EXPAND, border=1)
        # box_info.Add(picoo_btn, 1, flag=wx.EXPAND, border=1)
        # box_info.Add(tname, 1, flag=wx.EXPAND, border=1)
        panelinfo.SetSizer(box_info)

        elbow = energetic(self.data[0]['时间'])

        print('elbow=', elbow)

        self.disa_panel = self.create_disa_panel(panel)

        box = wx.BoxSizer(wx.VERTICAL)

        box.AddSpacer(5)

        box.Add(panelsearch, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=1)

        box.Add(panelinfo, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=1)

        box.Add(self.disa_panel, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=2)
        # box.Add(img_pic, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=2)

        box.AddSpacer(5)

        font3 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD, False)
        font4 = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.BOLD, False)

        picoo_btn.SetFont(font3)
        tname.SetFont(font3)
        picoo_btn_st.SetFont(font3)
        tname_st.SetFont(font3)
        addtrans.SetFont(font3)
        modifytrans.SetFont(font3)
        picbutton.SetFont(font3)
        button.SetFont(font3)
        trans.SetFont(font3)
        pole.SetFont(font3)
        trans_st.SetFont(font3)
        pole_st.SetFont(font3)
        choice2.SetFont(font3)
        choice2_time.SetFont(font3)
        search_btn.SetFont(font3)
        search2_btn.SetFont(font3)
        # print('self.data2=', self.data2)
        panel.SetSizer(box)

        # ----------------判断时间-------------------
        marty = time.localtime()
        malt_newtrue = int(time.strftime("%d", marty))

        # print('malt_newtrue=', malt_newtrue)
        '''
        if 25 <= malt_newtrue <= 30:
            print(type(malt_newtrue))
            print('ok')
        else:
            print('bad')
        '''
        '''
        if 25 <= malt_newtrue <= 27:
            outsqlite()
            print('backup_ok')
        '''


    '''

    # ---------更新图片Start----------------

    # 办公室电脑布局

    def __init__(self, parent):
        # self.on_Radiot_click = None
        self.on_Radiot_click = None
        self.data = settings.PRODUCTS
        self.data2 = settings.PRODUCTSALL
        # wx.Frame.__init__(self, None, -1, '【配网自动成图】', size=(900, 760))
        holder = settings.holder
        version = settings.version
        # self.SetStatusText("Elenut All Rights Reserved. Copyright © 2020.02" + '   Version=1.1.2')

        # wx.Frame.__init__(self, None, -1, '【配网自动成图】- ' + holder + version, size=(1340, 820))

        wx.Frame.__init__(self, None, -1, '【配网自动成图】- ' + holder + version, size=(1680, 1010))

        ico = wx.Icon("resources/bats.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        # panel = wx.Panel(self, wx.Center, size=(1340, 10))

        panel = wx.Panel(self, wx.Center, size=(1650, 10))

        self.SetBackgroundColour('#f5f5d5')
        # ----------------------
        # panelsearch = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        panelsearch = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1650, -1))

        choice2 = wx.TextCtrl(panelsearch, name="choice2", value=settings.lname + '   ' + settings.tname,
                              size=(1300, 30), style=wx.TE_CENTER)

        choice2.Bind(wx.EVT_RIGHT_DOWN, self.OnEnterWindow)  # 2 绑定鼠标位于其上事件

        choice2_time = wx.TextCtrl(panelsearch, name="choice2_time", value=settings.company, size=(90, 30),
                                   style=wx.TE_CENTER)
        choice2_time.Bind(wx.EVT_RIGHT_DOWN, self.OnEnterCompany)  # 2 绑定鼠标位于其上事件

        search2_btn = wx.Button(parent=panelsearch, label="手气不错", size=wx.Size(70, 30))
        self.Bind(wx.EVT_BUTTON, self.search2_btn_onclick, search2_btn)

        search_btn = wx.Button(parent=panelsearch, label="搜索", size=wx.Size(80, 30))
        self.Bind(wx.EVT_BUTTON, self.search_btn_onclick, search_btn)
        boxsearch = wx.BoxSizer(wx.HORIZONTAL)
        boxsearch.AddSpacer(1)  # 添加空白

        boxsearch.Add(search2_btn, 1, flag=wx.ALL | wx.FIXED_MINSIZE, border=1)

        boxsearch.Add(choice2, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        boxsearch.Add(choice2_time, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        boxsearch.Add(search_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=0)

        panelsearch.SetSizer(boxsearch)
        # --------------------------------------------------------

        # panelinfo = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1340, -1))

        panelinfo = wx.Panel(panel, pos=(50, 2), style=wx.BORDER_DOUBLE, size=wx.Size(1650, -1))

        picoo_btn_st = wx.StaticText(panelinfo, label="线路名称:", size=(80, 30), style=wx.TE_LEFT | wx.Center)
        picoo_btn = wx.TextCtrl(panelinfo, name="gchoice", value=settings.lname, size=(200, 30), style=wx.BU_LEFT)
        # picoo_btn = wx.TextCtrl(panelinfo, name="choice", value='南大线', size=(260, 20), style=wx.BU_LEFT)
        tname_st = wx.StaticText(panelinfo, label="设备型号:", size=(80, 30), style=wx.TE_LEFT | wx.Center)
        tname = wx.TextCtrl(panelinfo, name="capacity", value=settings.capacity, size=(200, 30), style=wx.BU_LEFT)

        picbutton = wx.Button(panelinfo, label="导入数据", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.uploadPhoto, picbutton)

        addtrans = wx.Button(panelinfo, label="新增设备", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.Andtrans, addtrans)

        modifytrans = wx.Button(panelinfo, label="更新数据", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.Modifytrans, modifytrans)

        button = wx.Button(panelinfo, label="配网成图", size=(80, 30))
        self.Bind(wx.EVT_BUTTON, self.showgram, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        boxh = wx.BoxSizer(wx.HORIZONTAL)

        boxh.Add(picbutton, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=1)
        boxh.AddSpacer(15)
        boxh.Add(addtrans, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(15)
        boxh.Add(picoo_btn_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(picoo_btn, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(15)

        # -----------------
        trans_st = wx.StaticText(panelinfo, label="设备名称:", size=(80, 30), style=wx.TE_LEFT)
        trans = wx.TextCtrl(panelinfo, name="tname", value=settings.tname, size=(200, 30), style=wx.BU_LEFT)
        trans.Bind(wx.EVT_RIGHT_DOWN, self.OnEntertrans)

        pole_st = wx.StaticText(panelinfo, label="杆号路径:", size=(80, 30), style=wx.TE_LEFT)
        pole = wx.TextCtrl(panelinfo, name="pole", value=settings.pole, size=(200, 30), style=wx.BU_LEFT)

        chearray = wx.CheckBox(panelinfo, label='Original', size=(50, 30), style=wx.BU_LEFT, name="checkpole")
        chearray.SetValue(settings.checkpole)

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)

        boxh.Add(trans_st, 0, flag=wx.FIXED_MINSIZE | wx.ALIGN_LEFT | wx.ALL, border=1)
        boxh.Add(trans, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(tname_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(tname, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(pole_st, 1, flag=wx.EXPAND, border=1)
        boxh.Add(pole, 1, flag=wx.EXPAND, border=1)

        boxh.AddSpacer(10)
        boxh.Add(chearray, 1, flag=wx.FIXED_MINSIZE | wx.ALIGN_LEFT | wx.ALL, border=1)



        boxh.Add(button, 1, flag=wx.EXPAND, border=1)
        boxh.AddSpacer(10)
        boxh.Add(modifytrans, 1, flag=wx.EXPAND, border=1)
        box_info = wx.BoxSizer(wx.VERTICAL)

        box_info.Add(boxh, 1, flag=wx.EXPAND, border=0)
        box_info.AddSpacer(10)
        # box_info.Add(boxt, 1, flag=wx.EXPAND, border=1)
        # box_info.AddSpacer(10)
        # box_info.Add(boxm, 1, flag=wx.EXPAND, border=1)
        # box_info.Add(picoo_btn, 1, flag=wx.EXPAND, border=1)
        # box_info.Add(tname, 1, flag=wx.EXPAND, border=1)
        panelinfo.SetSizer(box_info)

        elbow = energetic(self.data[0]['时间'])

        print('elbow=', elbow)

        self.disa_panel = self.create_disa_panel(panel)

        box = wx.BoxSizer(wx.VERTICAL)

        box.AddSpacer(5)

        box.Add(panelsearch, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=1)

        box.Add(panelinfo, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=1)

        box.Add(self.disa_panel, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=2)
        # box.Add(img_pic, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=2)

        box.AddSpacer(5)

        font3 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD, False)
        font4 = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.BOLD, False)
        picoo_btn.SetFont(font3)
        tname.SetFont(font3)
        picoo_btn_st.SetFont(font3)
        tname_st.SetFont(font3)
        addtrans.SetFont(font3)
        modifytrans.SetFont(font3)
        picbutton.SetFont(font3)
        button.SetFont(font3)
        trans.SetFont(font3)
        pole.SetFont(font3)
        trans_st.SetFont(font3)
        pole_st.SetFont(font3)
        choice2.SetFont(font3)
        choice2_time.SetFont(font3)
        search_btn.SetFont(font3)
        search2_btn.SetFont(font3)
        # print('self.data2=', self.data2)
        panel.SetSizer(box)

        # 创建底部的状态栏
    
        # ---------更新图片Start----------------
    '''

    def OnEnterWindow(self, event):
        farr = time.localtime()
        faulted_time = time.strftime("%Y", farr)

        faulted_time = ''
        choice = self.FindWindowByName('choice2')
        choice.Clear()

        # choice_time = self.FindWindowByName('choice2_time')
        # choice_time.SetValue(faulted_time)
        event.Skip()





    def onChecked(self, e):
        cb = e.GetEventObject()


        settings.checkpole = cb.GetValue()


        print('check_poles =', cb.GetValue())



    def OnEnterCompany(self, event):

        faulted_time = ''
        choicetime = self.FindWindowByName('choice2_time')
        choicetime.Clear()
        event.Skip()

    def OnEntertrans(self, event):

        trans_new = ''
        transnew_st = self.FindWindowByName('tname')
        transnew_st.Clear()
        event.Skip()

    def refresh_btn_onclick(self, event):
        PRODUCTS2 = []
        PRODUCTSALL = []
        PRODUCTSZSS2 = []
        settings.PRODUCTS = []

        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()
        sql = "select  * from faulty"
        cur.execute(sql)
        total = cur.fetchall()
        print('len(total)=', len(total))
        conn.commit()
        conn.close()
        for z in range(len(total)):
            a1 = total[z][1]
            a2 = total[z][2]
            a3 = total[z][3]
            a4 = total[z][4]
            a5 = total[z][5]
            a6 = total[z][6]
            a7 = total[z][7]
            a8 = total[z][8]
            a9 = total[z][9]
            a10 = total[z][10]
            a11 = total[z][11]
            a12 = total[z][12]
            a13 = total[z][13]
            a14 = total[z][14]
            a15 = total[z][15]
            a16 = total[z][16]
            a17 = total[z][17]
            a18 = total[z][18]
            a19 = total[z][19]
            a20 = total[z][20]
            a21 = total[z][21]
            a22 = total[z][22]
            a23 = total[z][23]
            a24 = total[z][24]
            a25 = total[z][25]
            a26 = total[z][26]
            a27 = total[z][27]
            a28 = total[z][28]
            a29 = total[z][29]
            a30 = total[z][30]
            a31 = total[z][31]

            PRODUCTSALL.append(
                {'时间': a1, '县公司': a2, '线路名称': a3, '故障电流Ia': a4, '故障电流Ib': a5, '故障电流Ic': a6, '故障线电压': round(a7, 3),
                 '线路负荷电流': a8, '线路负荷功率因数': round(a9, 3), '主变负荷电流': a10, '主变负荷功率因数': a11, '电站助增机组容量': a12, '主线总长': a13,
                 '故障类型': a14,
                 '一次短路电流': round(a15, 3), '故障阻抗': round(a16, 3), '弧光阻抗': round(a17, 3), '金属故障中心位置': round(a18, 3),
                 '弧光故障中心位置': round(a19, 3),
                 '电缆故障中心位置': round(a20, 3), '实际故障位置': round(a21, 3), '金属故障位置误差': round(a22, 3),
                 '弧光故障位置误差': round(a23, 3),
                 '电缆故障位置误差': round(a24, 3), '故障信息': a25, })
            PRODUCTS2.append(
                {'时间': a1, '线路名称': a3, '一次短路电流': round(a15, 3), '主线总长': float(a13), '故障类型': a14,
                 '金属故障中心位置': round(a18, 3),
                 '弧光故障中心位置': round(a19, 3), '电缆故障中心位置': round(a20, 3), '实际故障位置': round(a21, 3),
                 '故障误差': "{:.2%}".format(min(a22, a23, a24)), '故障信息': a25})
        # settings.PRODUCTS = PRODUCTS2
        settings.PRODUCTSALL = PRODUCTSALL
        # settings.PRODUCTSALL = random.sample(PRODUCTSALL, 6)
        # 随机展示前20组中的6组数据

        if len(PRODUCTS2) > 8:

            # settings.PRODUCTS = settings.PRODUCTS.append(random.sample(PRODUCTS2, len(PRODUCTS2)))
            settings.PRODUCTS = random.sample(PRODUCTS2, 8)
        else:
            settings.PRODUCTS = random.sample(PRODUCTS2, len(PRODUCTS2))

        print('PRODUCTSALL=', PRODUCTSALL)
        print('PRODUCTS2[0]=', PRODUCTS2[0])

        choice = self.FindWindowByName('gchoice')

        choice.SetValue(str(self.data[0]['线路名称']))

    def create_disa_panel(self, parent):
        choice = self.FindWindowByName('gchoice')
        tname = self.FindWindowByName('tname')
        choice_test = format(choice.GetValue())
        tname_test = format(tname.GetValue())

        cond = sqlite3.connect("fault.db3")
        cud = cond.cursor()
        sqm = "select  tname from transz where trim(mpolepath) != ''  and lname='" + str(choice_test) + "'"
        cud.execute(sqm)
        totall = cud.fetchall()
        total = len(totall)
        print('totall = ', totall)
        print('totaltransz = ', total)
        cond.commit()
        cond.close()

        if total:
            pass
        else:
            print('luoyeanling')
            polemodify(choice_test)

        panelx = wx.Panel(parent)
        panely = CanvasPanel(panelx)
        panely.draw()
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(panely, 1, flag=wx.ALIGN_CENTER | wx.ALL, border=2)
        panelx.SetSizer(box)
        return panelx

    def search_btn_onclick(self, parent):

        """查询按钮"""
        gchoice = self.FindWindowByName('gchoice')

        choice2 = self.FindWindowByName('choice2')
        choice2_test = format(choice2.GetValue())
        choice5 = choice2_test.split()
        print('choice5=', choice5)

        company2 = self.FindWindowByName('choice2_time')
        company2_test = format(company2.GetValue())

        if len(choice5) >= 2:
            linname = choice5[0]
            trname = choice5[1]



        else:
            if choice5 and len(choice5) <= 1:
                linname = choice5[0]
                trname = ''
                settings.tname = ''
            else:
                linname = ''
                trname = ''

        print('linname=', linname)
        print('trname=', trname)

        try:
            conn = sqlite3.connect("fault.db3")
            cur = conn.cursor()
            # sql = "select  lname, tname, tcapacity, polepath from transz where lname like '" + '%' + str(linname) +'%' + "'"
            '''
            sql = "select  lname, tname, tcapacity, polepath from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "'"
            '''

            '''
            sql = "select  lname, tname, company, tcapacity, polepath from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' and tcapacity like  '" + str(
                'S') + '%' + "'"
            '''

            sql = "select  lname, tname, company, tcapacity, polepath, allline_length from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "'"

            cur.execute(sql)
            totalchoseall = cur.fetchall()

            totalchose = random.sample(totalchoseall, 1)[0]
            print('totalchose=', totalchose)

            linname = totalchose[0]

            trname = totalchose[1]

            ltrname = totalchose[5]
            # gchoice.SetValue(trname)

            conn.commit()
            conn.close()
        except:
            ltrname = ''
            msg3 = "无此线路或配变!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框
        '''
        if (len(choice1) == 2 and (
                    choice1[0] in Line_result and choice1[1] in Line_result) and choice_time_test in a1) or (
                    choice_time_test in Line_result and choice_test in Line_result):
        '''

        gchoice = self.FindWindowByName('gchoice')
        gchoice.SetValue(linname)

        gtname = self.FindWindowByName('tname')
        gtname.SetValue(trname)

        settings.lname = linname
        settings.tname = trname
        settings.ltname = ltrname

        choice = self.FindWindowByName('gchoice')
        tname = self.FindWindowByName('tname')
        choice_test = format(choice.GetValue())
        tname_test = format(tname.GetValue())

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()

        try:
            sqe = "select  polepath, tcapacity, company from transz where tname ='" + str(
                tname_test) + "'and lname = '" + str(
                choice_test) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            npole = output_polepath(fpole[0])
            print('npole=', npole)
            ntcapacity = fpole[1]
            print('ntcapacity=', ntcapacity)
            ncompany = fpole[2]
            print('ncompany=', ncompany)
            cone.commit()
            cone.close()
            nipole = self.FindWindowByName('pole')
            nipole.SetValue(npole)
            nicapacity = self.FindWindowByName('capacity')
            nicapacity.SetValue(ntcapacity)
            settings.capacity = ntcapacity
            settings.pole = npole

            company2 = self.FindWindowByName('choice2_time')
            # company2_test = format(company2.GetValue())

            company2_test = ncompany
            settings.company = company2_test

            self.Destroy()
            krame = Disframe(None)
            krame.Show()

            choice = self.FindWindowByName('gchoice')
            choice.SetValue(settings.lname)
            trname = self.FindWindowByName('tname')
            trname.SetValue(settings.tname)
            capacity = self.FindWindowByName('capacity')
            capacity.SetValue(settings.capacity)
            pole = self.FindWindowByName('pole')
            pole.SetValue(settings.pole)
            compan = self.FindWindowByName('choice2_time')
            compan.SetValue(settings.company)


        except:
            pass
            '''
            msg3 = "无此线路或配变!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框
            '''

    # 手气不错搜索
    '''
    def search2_btn_onclick(self, parent):

        """查询按钮"""
        choice2 = self.FindWindowByName('choice2')
        choice2_test = ''
        choice5 = choice2_test.split()
        print('choice5=', choice5)

        company2 = self.FindWindowByName('choice2_time')
        company2_test = ''

        if len(choice5) >= 2:
            linname = choice5[0]
            trname = choice5[1]
        else:
            if choice5 and len(choice5) <= 1:
                linname = choice5[0]
                trname = ''
            else:
                linname = ''
                trname = ''

        print('linname=', linname)
        print('trname=', trname)

        try:
            conn = sqlite3.connect("fault.db3")
            cur = conn.cursor()
            # sql = "select  lname, tname, tcapacity, polepath from transz where lname like '" + '%' + str(linname) +'%' + "'"
            
            sql = "select  lname, tname, company, tcapacity, polepath, allline_length, from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' and tcapacity like  '" + str(
                'S') + '%' + "'"

            cur.execute(sql)
            totalchoseall = cur.fetchall()

            totalchose = random.sample(totalchoseall, 1)[0]
            print('totalchose=', totalchose)

            linname = totalchose[0]
            trname = totalchose[1]

            ltrname = totalchose[5]

            print('ltrname=', ltrname)

            conn.commit()
            conn.close()
        except:
            msg3 = "无此线路或配变!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框
            ltrname = ''
        

        gchoice = self.FindWindowByName('gchoice')
        gchoice.SetValue(linname)

        gtname = self.FindWindowByName('tname')
        gtname.SetValue(trname)

        settings.lname = linname
        settings.tname = trname

        settings.ltname = ltrname




        choice = self.FindWindowByName('gchoice')
        tname = self.FindWindowByName('tname')
        choice_test = format(choice.GetValue())
        tname_test = format(tname.GetValue())

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()

        try:
            sqe = "select  polepath, tcapacity, company from transz where tname ='" + str(
                tname_test) + "'and lname = '" + str(
                choice_test) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            npole = output_polepath(fpole[0])
            print('npole=', npole)
            ntcapacity = fpole[1]
            print('ntcapacity=', ntcapacity)
            ncompany = fpole[2]
            print('ncompany=', ncompany)
            cone.commit()
            cone.close()
            nipole = self.FindWindowByName('pole')
            nipole.SetValue(npole)
            nicapacity = self.FindWindowByName('capacity')
            nicapacity.SetValue(ntcapacity)
            settings.capacity = ntcapacity
            settings.pole = npole

            company2 = self.FindWindowByName('choice2_time')
            # company2_test = format(company2.GetValue())

            company2_test = ncompany
            settings.company = company2_test

            self.Destroy()
            krame = Disframe(None)
            krame.Show()

            choice = self.FindWindowByName('gchoice')
            choice.SetValue(settings.lname)
            trname = self.FindWindowByName('tname')
            trname.SetValue(settings.tname)
            capacity = self.FindWindowByName('capacity')
            capacity.SetValue(settings.capacity)
            pole = self.FindWindowByName('pole')
            pole.SetValue(settings.pole)
            compan = self.FindWindowByName('choice2_time')
            compan.SetValue(settings.company)


        except:
            msg3 = "数据错误！请检查！"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

            self.Destroy()
            krame = Disframe(None)
            krame.Show()
            # pass
            
    '''

    def search2_btn_onclick(self, parent):

        """查询按钮"""
        choice2 = self.FindWindowByName('choice2')
        choice2_test = ''
        choice5 = choice2_test.split()
        print('choice5=', choice5)

        company2 = self.FindWindowByName('choice2_time')
        company2_test = ''

        if len(choice5) >= 2:
            linname = choice5[0]
            trname = choice5[1]
        else:
            if choice5 and len(choice5) <= 1:
                linname = choice5[0]
                trname = ''
            else:
                linname = ''
                trname = ''

        print('linname=', linname)
        print('trname=', trname)

        try:
            conn = sqlite3.connect("fault.db3")
            cur = conn.cursor()
            # sql = "select  lname, tname, tcapacity, polepath from transz where lname like '" + '%' + str(linname) +'%' + "'"
            '''
            sql = "select  lname, tname, tcapacity, polepath from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "'"
            '''

            sql = "select  lname, tname, company, tcapacity, polepath, allline_length from transz where lname like '" + '%' + str(
                linname) + '%' + "' and tname like  '" + '%' + str(
                trname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' or lname like  '" + '%' + str(
                trname) + '%' + "' and tname like  '" + '%' + str(
                linname) + '%' + "' and company like  '" + '%' + str(
                company2_test) + '%' + "' and tcapacity like  '" + str(
                'S') + '%' + "'"

            cur.execute(sql)
            totalchoseall = cur.fetchall()

            totalchose = random.sample(totalchoseall, 1)[0]
            print('totalchose=', totalchose)

            linname = totalchose[0]
            trname = totalchose[1]

            ltrname = totalchose[5]

            conn.commit()
            conn.close()
        except:
            msg3 = "无此线路或配变!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框
            ltrname = ''

        gchoice = self.FindWindowByName('gchoice')
        gchoice.SetValue(linname)

        gtname = self.FindWindowByName('tname')
        gtname.SetValue(trname)

        settings.lname = linname
        settings.tname = trname

        settings.ltname = ltrname

        choice = self.FindWindowByName('gchoice')
        tname = self.FindWindowByName('tname')
        choice_test = format(choice.GetValue())
        tname_test = format(tname.GetValue())

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()

        try:
            sqe = "select  polepath, tcapacity, company from transz where tname ='" + str(
                tname_test) + "'and lname = '" + str(
                choice_test) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            npole = output_polepath(fpole[0])
            print('npole=', npole)
            ntcapacity = fpole[1]
            print('ntcapacity=', ntcapacity)
            ncompany = fpole[2]
            print('ncompany=', ncompany)
            cone.commit()
            cone.close()
            nipole = self.FindWindowByName('pole')
            nipole.SetValue(npole)
            nicapacity = self.FindWindowByName('capacity')
            nicapacity.SetValue(ntcapacity)
            settings.capacity = ntcapacity
            settings.pole = npole

            company2 = self.FindWindowByName('choice2_time')
            # company2_test = format(company2.GetValue())

            company2_test = ncompany
            settings.company = company2_test

            self.Destroy()
            krame = Disframe(None)
            krame.Show()

            choice = self.FindWindowByName('gchoice')
            choice.SetValue(settings.lname)
            trname = self.FindWindowByName('tname')
            trname.SetValue(settings.tname)
            capacity = self.FindWindowByName('capacity')
            capacity.SetValue(settings.capacity)
            pole = self.FindWindowByName('pole')
            pole.SetValue(settings.pole)
            compan = self.FindWindowByName('choice2_time')
            compan.SetValue(settings.company)


        except:
            msg3 = "数据错误！请检查！"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

            self.Destroy()
            krame = Disframe(None)
            krame.Show()

    def search_engine(self, parent):

        """查询按钮"""
        choice = self.FindWindowByName('gchoice')
        tname = self.FindWindowByName('tname')
        choice_test = format(choice.GetValue())
        tname_test = format(tname.GetValue())

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()

        try:
            sqe = "select  polepath, tcapacity from transz where tname ='" + str(tname_test) + "'and lname = '" + str(
                choice_test) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            npole = fpole[0]
            print('npole=', npole)
            ntcapacity = fpole[1]
            print('ntcapacity=', ntcapacity)
            cone.commit()
            cone.close()
            nipole = self.FindWindowByName('pole')
            nipole.SetValue(npole)
            nicapacity = self.FindWindowByName('capacity')
            nicapacity.SetValue(ntcapacity)
        except:

            msg3 = "无此线路或配变!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

    def showgram(self, parent):

        choice = self.FindWindowByName('gchoice')
        choice_test = format(choice.GetValue())
        trname = self.FindWindowByName('tname')
        trname_test = format(trname.GetValue())

        capa = self.FindWindowByName('capacity')
        capa_test = format(capa.GetValue())
        popath = self.FindWindowByName('pole')
        popath_test = format(popath.GetValue())

        settings.lname = choice_test
        settings.tname = trname_test
        settings.capacity = capa_test
        settings.pole = popath_test

        cone = sqlite3.connect("fault.db3")
        cue = cone.cursor()
        sqe = "select  * from transz where  lname = '" + str(choice_test) + "'"
        cue.execute(sqe)
        totalinf = cue.fetchone()

        cone.commit()
        cone.close()

        # totaline = len(totalinf)
        if totalinf:
            fcompany = totalinf[2]
            settings.company = fcompany

            ftransformer = totalinf[3]

            # 去除搜索圆圈

            if trname_test == '':
                settings.tname = ''
                settings.atname1 = ''
                settings.mtname2 = ''
                settings.atname2 = ''
                settings.mtname3 = ''
                settings.atname3 = ''
            else:
                settings.tname = ftransformer

            fcapacity = totalinf[5]
            settings.capacity = fcapacity

            fpole = totalinf[9]
            settings.pole = fpole

            # settings.chosen = ''

            self.Destroy()
            krame = Disframe(None)
            krame.Show()

            choice = self.FindWindowByName('gchoice')
            choice.SetValue(settings.lname)

            compan = self.FindWindowByName('choice2_time')
            compan.SetValue(settings.company)

            trname = self.FindWindowByName('tname')
            trname.SetValue(settings.tname)
            capacity = self.FindWindowByName('capacity')
            capacity.SetValue(settings.capacity)
            pole = self.FindWindowByName('pole')
            pole.SetValue(settings.pole)

            checkpole = self.FindWindowByName('checkpole')
            checkpole.SetValue(settings.checkpole)


            # settings.checkpole = False



        else:
            msg2 = "无此线路!"
            dialog = wx.MessageDialog(self, msg2, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

    def Andtrans(self, event):
        choice = self.FindWindowByName('gchoice')
        choice_test = format(choice.GetValue())
        trname = self.FindWindowByName('tname')
        trname_test = format(trname.GetValue())
        capa = self.FindWindowByName('capacity')
        capa_test = format(capa.GetValue())
        popath = self.FindWindowByName('pole')

        popath_test0 = format(popath.GetValue())
        popath_test = intput_polepath(popath_test0)

        settings.lname = choice_test
        settings.tname = trname_test
        settings.capacity = capa_test
        settings.pole = popath_test

        # --------------
        conn = sqlite3.connect("fault.db3")
        cum = conn.cursor()
        sqt = "select  company from line where lname='" + str(choice_test) + "'"
        cum.execute(sqt)
        oneitem = cum.fetchone()
        # print('oneitem=', oneitem)
        if oneitem:

            company = oneitem[0]
            print('company=', company)
        else:
            company = ''

        conn.commit()
        conn.close()
        # ---------------



        fty = time.localtime()

        conn = sqlite3.connect("fault.db3")
        cur = conn.cursor()

        sqt = "select  * from transz"
        cur.execute(sqt)
        totalout = len(cur.fetchall())
        print('totalout=', totalout)

        transz_time = str(time.strftime("%Y%m%d%H%M", fty)) + str(totalout)

        # 判别数据正确性
        trans_correct = popath_test.replace('F', '').replace('H', '').replace('X', '').replace('T', '').replace('Z', '').replace('Y','').replace(
            'L', '').replace('&', '').replace('^', '')
        trans_correct1 = trans_correct.replace('.', '')

        if company and '-' in capa_test and trans_correct1.isdecimal():

            try:
                if 'B' in capa_test:
                    cur.execute(
                        "INSERT INTO transz VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        [totalout + 1, 'Breaker', company, trname_test, transz_time, capa_test, choice_test,
                         'LGJ-400.LGJ-400', '0.0', popath_test, '0.01', '0.01', '0.01', '80.01', '0.01', '0.01', '0.01',
                         '0.01',
                         '80.01', '0.01', '80.01', '0.01', '80.01', '', 0.0,
                         0.0,
                         0.0, 0.0, '', '', '', popath_test, '', ''])
                else:
                    cur.execute(
                        "INSERT INTO transz VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        [totalout + 1, 'Transformer', company, trname_test, transz_time, capa_test, choice_test,
                         'LGJ-400.LGJ-400', '0.0', popath_test, '0.01', '0.01', '0.01', '80.01', '0.01', '0.01', '0.01',
                         '0.01',
                         '80.01', '0.01', '80.01', '0.01', '80.01', '', 0.0,
                         0.0,
                         0.0, 0.0, '', '', '', popath_test, '', ''])
                conn.commit()
                conn.close()

                polemodify(choice_test)
                # disgram(choice_test)

                self.Destroy()
                krame = Disframe(None)
                krame.Show()

                choice = self.FindWindowByName('gchoice')
                choice.SetValue(settings.lname)
                trname = self.FindWindowByName('tname')
                trname.SetValue(settings.tname)
                capacity = self.FindWindowByName('capacity')
                capacity.SetValue(settings.capacity)
                pole = self.FindWindowByName('pole')
                pole.SetValue(settings.pole)

                msg2 = "成功新增!"
                dialog = wx.MessageDialog(self, msg2, "提示!")
                dialog.ShowModal()  # 显示对话框
                dialog.Destroy()  # 销毁对话框
            except:
                pass
        else:
            msg2 = "数据错误或已有配变!"
            dialog = wx.MessageDialog(self, msg2, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

        # disgram(choice_test)

    def Modifytrans(self, event):

        choice = self.FindWindowByName('gchoice')
        choice_test = format(choice.GetValue())
        trname = self.FindWindowByName('tname')
        trname_test = format(trname.GetValue())
        capa = self.FindWindowByName('capacity')
        capa_test = format(capa.GetValue())
        popath = self.FindWindowByName('pole')

        popath_test0 = format(popath.GetValue())

        popath_test = intput_polepath(popath_test0)

        settings.lname = choice_test
        settings.tname = trname_test
        settings.capacity = capa_test
        settings.pole = popath_test0

        fty = time.localtime()
        print('choice_test=', choice_test)
        print('trname_test=', trname_test)

        try:
            try:
                # --------------
                conn = sqlite3.connect("fault.db3")
                cum = conn.cursor()

                sqt = "select  polepath, tcapacity, company from transz where tname ='" + str(
                    trname_test) + "'and lname = '" + str(
                    choice_test) + "'"

                # sqt = "select  * from transz where lname='" + str(choice_test) + "'"
                cum.execute(sqt)
                oneitem = cum.fetchone()
                conn.commit()
                print('totalout=', oneitem)
                print('okkkkkkkkkkkkkkkkkkk=')
                company = oneitem[2]
                print('company=', company)
            except:
                # 另外一种取县公司方法

                conn = sqlite3.connect("fault.db3")
                cum = conn.cursor()
                sqt = "select  company from line where lname ='" + str(choice_test) + "'"

                # sqt = "select  * from transz where lname='" + str(choice_test) + "'"
                cum.execute(sqt)
                oneitem = cum.fetchone()
                conn.commit()
                print('totalout=', oneitem)
                print('ooooooooooooooo=')
                company = oneitem[0]
                print('company=', company)

                # 另外一种取县公司方法

            # --------------------------

            #-------------判断数据合规性------------

            trans_correct = popath_test.replace('F', '').replace('H', '').replace('X', '').replace('T', '').replace('Z', '').replace(
                'Y', '').replace(
                'L', '').replace('&', '').replace('^', '')

            trans_correct1 = trans_correct.replace('.', '')

            if '-' in capa_test and trans_correct1.isdecimal():
                conn = sqlite3.connect("fault.db3")
                cur = conn.cursor()

                sqt = "select  * from transz"
                cur.execute(sqt)
                totalout = len(cur.fetchall())
                print('totalout=', totalout)

                transz_time = str(time.strftime("%Y%m%d%H%M", fty)) + str(totalout)

                cur.execute(
                    "UPDATE  transz SET tnumber=(?) where tname='" + str(trname_test) + "' and lname='" + str(
                        choice_test) + "'", [transz_time])
                cur.execute(
                    "UPDATE  transz SET tcapacity=(?) where tname='" + str(trname_test) + "' and lname='" + str(
                        choice_test) + "'", [capa_test])

                # 先将旧的进行保存
                # 预留一个函数进行旧的编号保存

                cur.execute(
                    "UPDATE  transz SET polepath=(?) where tname='" + str(trname_test) + "' and lname='" + str(
                        choice_test) + "'", [popath_test])

                '''
                cur.execute(
                    "UPDATE  transz SET brancher=(?) where tname='" + str(trname_test) + "' and lname='" + str(
                        choice_test) + "'", [popath_test])
                '''


                conn.commit()
                conn.close()

                polemodify(choice_test)

                # ----------------------------

                # disgram(choice_test)

                self.Destroy()
                krame = Disframe(None)
                krame.Show()

                choice = self.FindWindowByName('gchoice')
                choice.SetValue(settings.lname)
                trname = self.FindWindowByName('tname')
                trname.SetValue(settings.tname)
                capacity = self.FindWindowByName('capacity')
                capacity.SetValue(settings.capacity)
                pole = self.FindWindowByName('pole')
                pole.SetValue(settings.pole)

                # disgram(choice_test)

                msg2 = "成功更新!"
                dialog = wx.MessageDialog(self, msg2, "提示!")
                dialog.ShowModal()  # 显示对话框
                dialog.Destroy()  # 销毁对话框

            else:
                msg3 = "参数格式错误！请检查!"
                dialog = wx.MessageDialog(self, msg3, "提示!")
                dialog.ShowModal()  # 显示对话框
                dialog.Destroy()  # 销毁对话框

        except:
            msg3 = "更新失败!"
            dialog = wx.MessageDialog(self, msg3, "提示!")
            dialog.ShowModal()  # 显示对话框
            dialog.Destroy()  # 销毁对话框

    def OnCloseWindow(self, event):
        self.Destroy()

    def uploadPhoto(self, event):

        self.work = WorkThread()
        self.datapic = settings.PRODUCTS
        print('self.datapic', self.datapic)

    def pictures3_bltn_onclick(self, parent):

        print('self.data=', self.data)
        poultices = self.data[0]['时间']
        # poultices = '20200215131104'
        try:
            conn = sqlite3.connect("fault.db3")
            cur = conn.cursor()
            sql = "select * from picture where timestamp='" + poultices + "'"
            cur.execute(sql)
            total = cur.fetchone()
            stime3 = total[3]
            conn.commit()
            conn.close()
        except:
            stime3 = 'default.jpg'

        print('timestamp=', stime3)

        img_pathpicurl3 = stime3

        settings.pictured = img_pathpicurl3

        image = wx.Image('uploads\\' + str(settings.pictured), wx.BITMAP_TYPE_ANY)

        frame5 = Showpiece(image)
        frame5.Show()


'''
if __name__ == '__main__':
    app = wx.App()
    f = Disframe(None)
    f.Show(True)
    app.MainLoop()
'''
