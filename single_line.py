# cython: language_level=3
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Date    : 2022-10-25 00:23:45
# @Function: Auto-drawing single line diagram
# @Author  : Luo Xiaochun
# @Email   : luoxiaochun@proton.me
# @version : 1.1.0


import numpy as np
import matplotlib
import math

matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
import sqlite3
import wx


def polemodify(lrawname):
    # lname = '南大线'

    lname = lrawname

    def cgstring(xstring, dstring, z):

        zis = xstring.split(':')[0]

        zis0 = zis

        zis1 = zis0.split('.')

        # zis = '192^1.10^2.7.X&1^1'

        # 得到首数的指数值

        if '^' in zis.split('.')[z]:
            zsdata = '^' + zis.split('.')[z].split('^')[-1]
        else:
            zsdata = ''

        # 得到首数的类型符号

        if '&' in zis.split('.')[z]:
            zsdata2 = zis.split('.')[z].split('^')[0].split('&')[0] + '&'
        else:
            zsdata2 = ''

        zis1[z] = zis.split('.')[z].split('^')[0].split('&')[-1].replace(
            zis.split('.')[z].split('^')[0].split('&')[-1],
            str(dstring))

        zis1[z] = str(zsdata2) + zis1[z] + str(zsdata)
        # print('zis1[1]=', zis1[z])
        # zus1 = zis1[0] + ':' + '.'.join(zis1[1:]) + ':' + pallslave[i][j].split('.')[-1]
        zus1 = '.'.join(zis1[:z]) + '.' + '.'.join(zis1[z:]) + ':' + xstring.split(':')[-1]

        return zus1

    transz_all = []

    poleall = []

    poleall2 = []

    polepath = []
    tcapa = []
    tname = []
    line_name = []

    pole_last = []
    tcapa_last = []
    tname_last = []
    line_name_last = []

    polemax = []
    branchmax = []
    polebase = 20
    branchnum = 1

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()
    sqm = "select  * from transz where lname='" + str(lname) + "'"
    cud.execute(sqm)
    total = cud.fetchall()

    cond.commit()
    cond.close()

    for j in range(len(total)):

        # if float(total[j][5].split('-')[-1]) > 10:
        if 1:
            polemax_str = total[j][9]
            pole_str1 = polemax_str.split('.')
            pole_num = float((pole_str1[0].split('&')[-1]).split('^')[0])

            branch_num = len(pole_str1)
            branchmax.append(branch_num)

            polemax.append(pole_num)
            # print('polemax=', polemax)
            # polebase = int(0.618 * np.max(polemax))/0.618
            # polebase = int(0.618 * np.max(polemax)) / 0.618
            branchnum = np.max(branchmax)
            polebase = np.max(polemax)

            # polebase = int(70)
            poleallsig = []
            polesb = []
            for k in range(len(pole_str1)):
                poleallsig.append(pole_str1[k].split('^')[0].split('&')[-1])
            polesb = '.'.join(poleallsig) + '.' + total[j][4]
            poleall.append(polesb)

            # print('polebase=', polebase)

    allpole = []

    z = []
    for i in range(len(total)):
        # if float(total[i][5].split('-')[-1]) > -1:
        # if 1:
        # if float(total[i][5].split('-')[-1]) > 9:
        if float(total[i][5].split('-')[-1]) > 9 or total[i][1].split('.')[0] == 'Virtual':

            pole_str = total[i][9]
            pole_str1 = pole_str.split('.')
            pole_num = float((pole_str1[0].split('&')[-1]).split('^')[0])
            z.append(int((pole_str1[0].split('&')[-1]).split('^')[0]))
            # if float(total[i][9].split('.'))[1] < 50:

            poleallsig2 = []
            polesb2 = []
            for k in range(len(pole_str1)):
                poleallsig2.append(pole_str1[k].split('^')[0].split('&')[-1])
            polesb = '.'.join(poleallsig2) + '.' + total[i][4]
            poleall2.append(polesb)

            allpole.append('0.' + total[i][9])

            if pole_num <= polebase:
                line_name.append(total[i][6])
                polepath.append('0.' + total[i][9])
                tcapa.append(total[i][5])
                tname.append(total[i][3])
            else:
                line_name_last.append(total[i][6])
                pole_last.append('0.' + total[i][9])
                tcapa_last.append(total[i][5])
                tname_last.append(total[i][3])

    '''
    polemidnumber = int(0.618 * len(allpole))
    polepath = allpole
    pole_last = allpole[polemidnumber+1 : len(allpole)]
    '''
    # polepath = allpole
    #
    # polesort = sorted(poleall, key=lambda s: int(s.split('.')[0]))

    polesort = sorted(poleall2, key=lambda s: int(s.split('.')[0]))

    print('poleall=', poleall)
    print('polesort=', polesort)

    print('polepath=', polepath)
    print('pole_last=', pole_last)
    print('z=', z)

    print('branchnum=', branchnum)

    zlist = sorted(list(set(z)))

    # polepath = [0, 13, 156, 196, 222, 248, 251,500]

    # polepath = [0, 9, 10, 12, 14, 18, 19, 20, 22, 23, 24, 29, 35, 40, 44, 46, 59, 61, 62, 69, 125]

    # olepaths = [0, 18, 19, 45, 48, 115, 136, 184]

    # polepaths = zlist

    # polepa = sorted(zlist)

    z0 = [0]

    for r in range(len(polesort)):
        z0.append(int(polesort[r].split('.')[0]))

    polepa = z0

    print('polepa=', polepa)

    # --------------------------------------

    def virtual_poles(poles, zoo=2.0, shrin=2.0, kmody=1.0, k=5):
        polepaths = poles

        zoom = zoo
        shrink = shrin
        kegrate = kmody
        k = 10

        for i in range(k):
            dpolepath = [1]
            pole_shadow = [0]

            # print('polepaths=', polepaths)

            for j in range(1, len(polepaths)):
                if j > len(polepaths):
                    break
                else:
                    dpole = polepaths[j] - polepaths[j - 1]
                    dpolepath.append(dpole)
            # print('dpolepath=', dpolepath)

            for i in range(1, len(polepaths)):

                if polepaths[i] - polepaths[i - 1] > 0.5:

                    # 压缩得很密集 poles = pole_shadow[i - 1] + zoom / math.log(1.718 + kegrate * math.sqrt(dpolepath[i]))
                    '''
                    poles = pole_shadow[i - 1] + zoom / math.log(1.718 + kegrate * math.sqrt(dpolepath[i])) + shrink * math.log(
                        dpolepath[i])
                    '''
                    poles = pole_shadow[i - 1] + zoom / math.log(
                        2.718 + kegrate * math.sqrt(dpolepath[i])) + shrink * math.log(
                        0.367918 + math.sqrt(dpolepath[i]))

                    pole_shadow.append(math.floor(poles))
                else:
                    pole_shadow.append(pole_shadow[i - 1])
            polepaths = pole_shadow
            # print('pole_factua=', sorted(list(set(z))))
            # print('zlit_len=', len(list(set(z))))
            # print('pole_shadow=', pole_shadow)
            # print('pole_len=', len(pole_shadow))
        return pole_shadow[1:]

    # -------------------------------------

    polepab = virtual_poles(polepa, 2.0, 2.0, 1.0, 5)

    print('------------------坐标压缩后的优化值--------------------------------')
    print('polepa=', polepa)
    print('polepab=', polepab)
    print('------------------坐标压缩后的优化值--------------------------------')

    # print('polesortgame=', polesort)

    poleend = []

    for t in range(len(polepab)):
        polesb = (str(polepab[t])) + '.' + polesort[t].split('.')[-1]

        poleend.append(polesb)
    print('------------------坐标压缩后的优化值带编号-------------------------------')
    print('poleend=', poleend)
    print('------------------坐标压缩后的优化值带编号-------------------------------')

    print('polesort=', polesort)
    print('pole_len=', len(polepab))

    poleends = []

    soleends = []

    print('polesort_len=', len(polesort))

    print('polepath_len=', len(polepath))

    # 对polepath进行排序开始

    polepaths = sorted(polepath, key=lambda s: int((s.split('.')[1].split('^')[0].split('&')[-1])))

    print('polepaths=', polepaths)
    polepath = polepaths

    # 对polepath进行排序结束

    for g in range(len(polepath)):
        zas = polepath[g]
        zas1 = zas.split('.')

        zassog = '192^1.10^2.7.X&1^1'

        # 得到首数的指数值

        if '^' in zas.split('.')[1]:
            zsdata = '^' + zas.split('.')[1].split('^')[-1]
        else:
            zsdata = ''

        # 得到首数的类型符号

        if '&' in zas.split('.')[1]:
            zsdata2 = zas.split('.')[1].split('^')[0].split('&')[0] + '&'
        else:
            zsdata2 = ''

        # zsdataraw = str(zsdata2) + '&' + str(polepab[g]) + '^' + str( zsdata)

        # zas1[1] = zas.split('.')[1].split('^')[0].split('&')[-1].replace(zas.split('.')[1].split('^')[0].split('&')[-1], str(polepab[g]))

        zas1[1] = zas.split('.')[1].split('^')[0].split('&')[-1].replace(
            zas.split('.')[1].split('^')[0].split('&')[-1],
            str(polepab[g]))

        zas1[1] = str(zsdata2) + zas1[1] + str(zsdata)

        zbs1 = zas1[0] + ':' + '.'.join(zas1[1:]) + ':' + polesort[g].split('.')[-1]

        zcs1 = zas1[0] + ':' + '.'.join(zas1[1:])

        poleends.append(zbs1)

        soleends.append(zcs1)

    print('poleall=', poleall)

    print('polepath=', polepath)

    print('soleends=', soleends)

    print('poleends=', poleends)

    print('poleend_len=', len(poleend))
    print('polepath_len=', len(polepath))
    print('poleends_len=', len(poleends))

    # -------------------前述得到主线杆号变换后的值---------------------------------------------

    print('---------------------------------------------------------------------------------')
    print('一级支线杆号变换开始')
    print('poleends=', poleends)

    polemaster = sorted(list(set(polepab)))
    # 主线实际杆号顺序排列

    print('主线实际杆号排序')
    print('polemaster=', polemaster)

    # poleallslave = []
    # poleallnum = []

    # ---------------------问题部分-------------------

    poleallslave = []

    poleallnum = []

    for i in range(len(polemaster)):
        dp = polemaster[i]
        poleslave = []
        for j in range(len(poleends)):
            if str(dp) == (poleends[j].split(':')[1]).split('.')[0].split('^')[0].split('&')[-1]:
                if len((poleends[j].split(':')[1]).split('.')) == 1:
                    poleslave.append(poleends[j].split(':')[1] + '.0' + ':' + poleends[j].split(':')[2])
                    poleallnum.append(poleends[j].split(':')[1] + '.0' + ':' + poleends[j].split(':')[2])

                else:
                    poleslave.append(':'.join(poleends[j].split(':')[1:]))
                    poleallnum.append(':'.join(poleends[j].split(':')[1:]))
                    # poleslave.append(poleends[j].split(':')[1:])

                # poleslave.append(':'.join(poleends[j].split(':')[1:]))
            else:
                continue
        # print('poleslave=', poleslave)
        if poleslave:
            poleallslave.append(poleslave)

    print('poleallslave=', poleallslave)
    print('poleallnum=', poleallnum)

    print('\n')

    # print('poleallslave[1]=', poleallslave[0])

    # poleallslave[1]= ['2:2021022820184584', '2.1:2021022820184585', '2.2:2021022820184586', '2.4:2021022820184587', '2.5:2021022820184588', '2.5^1.1:2021022820184589', '2.5^1.13:2021022820184590', '2.5^2.5:2021022820184591']

    allslave = []

    for k in range(len(poleallslave)):
        poleslavesort = sorted(poleallslave[k],
                               key=lambda s: int((s.split(':')[0].split('.')[1]).split('^')[0].split('&')[-1]))
        allslave.append(poleslavesort)

    hpolepa = []

    for i in range(len(allslave)):

        # h0 = [0]
        h0 = [0]

        for r in range(len(allslave[i])):
            # if len(allslave[i]) > 1:
            if 1:
                h0.append(int(allslave[i][r].split(':')[0].split('.')[1].split('^')[0].split('&')[-1]))

                # print('h0=', h0)
        hpolepa.append([polemaster[i], h0])
        # print('hpolepa=', hpolepa)
        # print('hpolepa=', hpolepa)

    #  --------开始变换一级支线的虚拟杆号Start-------------

    allpoleslave = []
    for j in range(len(hpolepa)):
        poleslave1 = virtual_poles(hpolepa[j][1], zoo=2.0, shrin=2.0, kmody=1.5, k=5)
        allpoleslave.append([polemaster[j], poleslave1])

    print('allslave=', allslave)
    print('allpoleslave=', allpoleslave)

    #  --------开始变换一级支线的虚拟杆号End-------------

    print('一级支线杆号变换结束')
    print('---------------------------------------------------------------------------------')

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(poleallnum)):
        # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [poleallnum[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

        cud.execute("update transz  set mpolepath=(?) where tnumber =(?) and lname =(?)",
                    [poleallnum[i].split(':')[0], poleallnum[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    print('---------------------------------------------------------------------------------')
    print('一级支线杆号更新结束')

    # -------------二级支线编号调整开始----------------

    pallslave = allslave
    pallpoleslave = allpoleslave

    holdpole = []
    allholdpole = []

    beautypole = []

    for i in range(len(pallslave)):
        for j in range(len(pallslave[i])):
            # print('pallslave[i][j]=', pallslave[i][j])
            # print('pallpoleslave[i][j]=', str(pallpoleslave[i][0]) + '.' + str(pallpoleslave[i][1][j]) + ':' + str(pallslave[i][j].split(':')[-1]))

            # print('pallslave=', pallslave[i][j])

            # -----------核心-------------------------
            zis = pallslave[i][j].split(':')[0]
            zis1 = zis.split('.')

            zissog = '192^1.10^2.7.X&1^1'

            # 得到首数的指数值

            if '^' in zis.split('.')[1]:
                zsdata = '^' + zis.split('.')[1].split('^')[-1]
            else:
                zsdata = ''

            # 得到首数的类型符号

            if '&' in zis.split('.')[1]:
                zsdata2 = zis.split('.')[1].split('^')[0].split('&')[0] + '&'
            else:
                zsdata2 = ''

            # zsdataraw = str(zsdata2) + '&' + str(polepab[g]) + '^' + str( zsdata)

            # zas1[1] = zas.split('.')[1].split('^')[0].split('&')[-1].replace(zas.split('.')[1].split('^')[0].split('&')[-1], str(polepab[g]))

            zis1[1] = zis.split('.')[1].split('^')[0].split('&')[-1].replace(
                zis.split('.')[1].split('^')[0].split('&')[-1],
                str(pallpoleslave[i][1][j]))

            zis1[1] = str(zsdata2) + zis1[1] + str(zsdata)
            # print('zis1[1]=', zis1[1])
            # zus1 = zis1[0] + ':' + '.'.join(zis1[1:]) + ':' + pallslave[i][j].split('.')[-1]
            zus1 = zis1[0] + '.' + '.'.join(zis1[1:]) + ':' + pallslave[i][j].split(':')[-1]

            beautypole.append(zus1)

            holdpolek = str(pallpoleslave[i][0]) + '.' + str(pallpoleslave[i][1][j]) + ':' + str(
                pallslave[i][j].split(':')[-1])

            holdpole.append(holdpolek)

    print('---------------------------------------------------------------------------------')

    print('pallslave=', pallslave)

    print('allpoleslave=', allpoleslave)

    print('holdpole=', holdpole)

    print('polepathle=', polepath)
    print('beautypole=', beautypole)

    print('---------------------------------------------------------------------------------')

    # branchraw = holdpole

    branchraw = beautypole

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(branchraw)):
        # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [poleallnum[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

        cud.execute("update transz  set mpolepath=(?) where tnumber =(?) and lname =(?)",
                    [branchraw[i].split(':')[0], branchraw[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    # -------------二级支线编号调整结束----------------

    # beautypole = branchraw

    # -------------三级支线编号调整开始----------------

    poleya = polepath
    allpoleya = []
    for i in range(len(beautypole)):
        if len(beautypole[i].split(':')[0].split('.')) > 2:
            allpoleya.append(beautypole[i])
    print('allpoleya三级=', allpoleya)

    allpuma = []
    allpoleya0 = allpoleya
    tpole = [0]
    for t in range(len(allpoleya)):
        alltpole = []
        tpole.append('.'.join(allpoleya[t].split(':')[0].split('.')[0:2]))
        if tpole[t + 1] != tpole[t]:
            for p in range(len(allpoleya0)):
                if str(tpole[t + 1]) == '.'.join(allpoleya0[p].split(':')[0].split('.')[0:2]):
                    alltpole.append(allpoleya0[p])

        allpuma.append(alltpole)

    # 分组展示
    print(' allpuma=三级=', allpuma)

    allthird = []

    print('allpuma=', allpuma)

    for k in range(len(allpuma)):
        polesthird = sorted(allpuma[k],
                            key=lambda s: int((s.split(':')[0].split('.')[2]).split('^')[0].split('&')[-1]))
        allthird.append(polesthird)

    print('allthird=', allthird)
    # -------------三级支线编号调整结束----------------

    hpole3 = []
    hpole4 = []

    hpole5 = []
    for i in range(len(allthird)):

        # h0 = [0]
        h0 = [0]

        for r in range(len(allthird[i])):
            # if len(allslave[i]) > 1:
            if 1:
                h0.append(int(allthird[i][r].split(':')[0].split('.')[2].split('^')[0].split('&')[-1]))

        polesh0 = virtual_poles(h0, zoo=2.0, shrin=2.0, kmody=1.5, k=5)  # print('h0=', h0)
        hpole3.append([allthird[i], h0[1:]])

        # print('polesh0=', polesh0)
        for d in range(len(allthird[i])):
            if allthird[i][d]:
                hpole4.append([cgstring(allthird[i][d], polesh0[d], 2), polesh0[d]])
                hpole5.append(cgstring(allthird[i][d], polesh0[d], 2))

    print('hpole3=', hpole3)
    print('hpole4=', hpole4)

    print('hpole5=', hpole5)

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(hpole5)):
        # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [hpole5[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

        cud.execute("update transz  set mpolepath =(?) where tnumber =(?) and lname =(?)",
                    [hpole5[i].split(':')[0], hpole5[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    print('ok=')

    # -------------三级支线编号更新结束----------------

    beautypole = hpole5

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$=")
    print("beautypole=", beautypole)

    # -------------四级级支线编号调整开始----------------

    poleya4 = polepath
    allpoleya4 = []
    for i in range(len(beautypole)):
        if len(beautypole[i].split(':')[0].split('.')) > 3:
            allpoleya4.append(beautypole[i])
    print('allpoleya4=', allpoleya4)

    allpuma4 = []
    allpoleya40 = allpoleya4
    tpole = [0]
    for t in range(len(allpoleya4)):
        alltpole4 = []
        tpole.append('.'.join(allpoleya4[t].split(':')[0].split('.')[0:3]))
        if tpole[t + 1] != tpole[t]:
            for p in range(len(allpoleya40)):
                # if str(tpole[t + 1]) in allpoleya40[p].split(':')[0]:
                if str(tpole[t + 1]) == '.'.join(allpoleya40[p].split(':')[0].split('.')[0:3]):
                    alltpole4.append(allpoleya40[p])

        allpuma4.append(alltpole4)

    print(' allpuma4=', allpuma4)

    allfourth = []

    print('allpuma4=', allpuma4)

    for k in range(len(allpuma4)):
        polesfourth = sorted(allpuma4[k],
                             key=lambda s: int((s.split(':')[0].split('.')[3]).split('^')[0].split('&')[-1]))
        allfourth.append(polesfourth)

    print('allfourth=', allfourth)

    fhpole3 = []
    fhpole4 = []

    fhpole5 = []
    for i in range(len(allfourth)):

        # h0 = [0]
        h40 = [0]

        for r in range(len(allfourth[i])):
            # if len(allslave[i]) > 1:
            if 1:
                h40.append(int(allfourth[i][r].split(':')[0].split('.')[3].split('^')[0].split('&')[-1]))

        polesh40 = virtual_poles(h40, zoo=2.0, shrin=2.0, kmody=1.5, k=5)  # print('h0=', h0)

        fhpole3.append([allfourth[i], h40[1:]])

        # print('polesh0=', polesh0)
        for d in range(len(allfourth[i])):
            if allfourth[i][d]:
                fhpole4.append([cgstring(allfourth[i][d], polesh40[d], 3), polesh40[d]])
                fhpole5.append(cgstring(allfourth[i][d], polesh40[d], 3))

    print('fhpole3=', fhpole3)
    print('fhpole4=', fhpole4)
    print('fhpole5------=', hpole5)

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(fhpole5)):
        # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [hpole5[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

        cud.execute("update transz  set mpolepath =(?) where tnumber =(?) and lname =(?)",
                    [fhpole5[i].split(':')[0], fhpole5[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    print('ok=')
    # -------------四级级支线编号调整结束----------------

    # 2021.06.26 低级错误 beautypole = hpole5

    beautypole = fhpole5

    print('------------------pole5=', fhpole5)

    # -------------五级支线编号调整艰难开始----------------

    poleya5 = polepath
    allpoleya5 = []
    for i in range(len(beautypole)):
        if len(beautypole[i].split(':')[0].split('.')) > 4:
            allpoleya5.append(beautypole[i])
    print('allpoleya5=', allpoleya5)
    print('**************************pole5=', allpoleya5)
    allpuma5 = []
    allpoleya50 = allpoleya5
    tpole5 = [0]

    for t in range(len(allpoleya5)):
        alltpole5 = []
        tpole5.append('.'.join(allpoleya5[t].split(':')[0].split('.')[0:4]))
        print('tpole5_raw=', tpole5)
        print('alltpole5=', alltpole5)
        if tpole5[t + 1] != tpole5[t]:
            for p in range(len(allpoleya50)):
                # if str(tpole5[t + 1]) in allpoleya50[p].split(':')[0]:
                if str(tpole5[t + 1]) == '.'.join(allpoleya50[p].split(':')[0].split('.')[0:4]):
                    alltpole5.append(allpoleya50[p])

        # allpuma5.append(alltpole5)
        allpuma5.append(alltpole5)
    print('tpole5=', tpole5)
    print('allpuma5=', allpuma5)

    allfive = []

    print('allpuma5=', allpuma5)
    # ------------------

    for k in range(len(allpuma5)):
        polesfive = sorted(allpuma5[k],
                           key=lambda s: int((s.split(':')[0].split('.')[4]).split('^')[0].split('&')[-1]))
        allfive.append(polesfive)

    print('allfive=', allfive)

    fhpole7 = []
    fhpole8 = []
    fhpole9 = []

    for i in range(len(allfive)):

        # h0 = [0]
        h50 = [0]

        for r in range(len(allfive[i])):
            # if len(allslave[i]) > 1:
            if 1:
                h50.append(int(allfive[i][r].split(':')[0].split('.')[4].split('^')[0].split('&')[-1]))

        polesh50 = virtual_poles(h50, zoo=2.0, shrin=2.0, kmody=1.5, k=5)  # print('h0=', h0)
        fhpole7.append([allfive[i], h50[1:]])

        for d in range(len(allfive[i])):
            if allfive[i][d]:
                fhpole8.append([cgstring(allfive[i][d], polesh50[d], 4), polesh50[d]])
                fhpole9.append(cgstring(allfive[i][d], polesh50[d], 4))

    print('fhpole8××××××××=', fhpole8)
    print('fhpole9-----=', fhpole9)

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(fhpole9)):
        cud.execute("update transz  set mpolepath =(?) where tnumber =(?) and lname =(?)",
                    [fhpole9[i].split(':')[0], fhpole9[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    print('ok555555=')

    # -------------五级支线编号调整艰难结束-----------------

    beautypole = fhpole9
    # -----------------六级开始-----------

    poleya6 = polepath
    allpoleya6 = []
    for i in range(len(beautypole)):
        if len(beautypole[i].split(':')[0].split('.')) > 5:
            allpoleya6.append(beautypole[i])
    print('allpoleya6=', allpoleya6)
    print('**************************pole6=', allpoleya6)
    allpuma6 = []
    allpoleya60 = allpoleya6
    tpole6 = [0]

    for t in range(len(allpoleya6)):
        alltpole6 = []
        tpole6.append('.'.join(allpoleya6[t].split(':')[0].split('.')[0:5]))
        print('tpole6=', tpole6)
        print('alltpole6=', alltpole6)
        if tpole6[t + 1] != tpole6[t]:
            for p in range(len(allpoleya60)):
                # if str(tpole6[t + 1]) in allpoleya60[p].split(':')[0]:
                if str(tpole6[t + 1]) == '.'.join(allpoleya60[p].split(':')[0].split('.')[0:5]):
                    alltpole6.append(allpoleya60[p])
            allpuma6.append(alltpole6)
        # allpuma6.append(alltpole6)

    print('tpole6=', tpole6)
    print('allpuma6=', allpuma6)

    allsix = []

    print('allpuma6=', allpuma6)
    # ------------------

    for k in range(len(allpuma6)):
        polessix = sorted(allpuma6[k],
                          key=lambda s: int((s.split(':')[0].split('.')[5]).split('^')[0].split('&')[-1]))
        allsix.append(polessix)

    print('allsix=', allsix)

    fhpole10 = []
    fhpole11 = []
    fhpole12 = []

    for i in range(len(allsix)):

        # h0 = [0]
        h60 = [0]

        for r in range(len(allsix[i])):
            # if len(allslave[i]) > 1:
            if 1:
                h60.append(int(allsix[i][r].split(':')[0].split('.')[5].split('^')[0].split('&')[-1]))

        polesh60 = virtual_poles(h60, zoo=2.0, shrin=2.0, kmody=1.5, k=5)  # print('h0=', h0)
        fhpole10.append([allsix[i], h60[1:]])

        for d in range(len(allsix[i])):
            if allsix[i][d]:
                fhpole11.append([cgstring(allsix[i][d], polesh60[d], 5), polesh60[d]])
                fhpole12.append(cgstring(allsix[i][d], polesh60[d], 5))

    print('fhpole11=', fhpole11)
    print('fhpole12=', fhpole12)

    cond = sqlite3.connect("fault.db3")
    cud = cond.cursor()

    for i in range(len(fhpole12)):
        # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [hpole5[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

        cud.execute("update transz  set mpolepath =(?) where tnumber =(?) and lname =(?)",
                    [fhpole12[i].split(':')[0], fhpole12[i].split(':')[-1], str(lname)])

        cond.commit()

    cond.close()

    print('ok666666=')

    # -----------------六级结束---------


    # 核心函数编写--7级以上
    beautypoles = fhpole12

    def one_line(bpole, bnum):
        brnum = bnum
        beautypole = bpole
        allpoleya6 = []
        for i in range(len(beautypole)):
            if len(beautypole[i].split(':')[0].split('.')) > brnum:
                allpoleya6.append(beautypole[i])
        print('allpoleya6=', allpoleya6)
        print('**************************pole6=', allpoleya6)
        allpuma6 = []
        allpoleya60 = allpoleya6
        tpole6 = [0]

        for t in range(len(allpoleya6)):
            alltpole6 = []
            tpole6.append('.'.join(allpoleya6[t].split(':')[0].split('.')[0:brnum]))
            print('tpole6=', tpole6)
            print('alltpole6=', alltpole6)
            if tpole6[t + 1] != tpole6[t]:
                for p in range(len(allpoleya60)):
                    # if str(tpole6[t + 1]) in allpoleya60[p].split(':')[0]:
                    if str(tpole6[t + 1]) == '.'.join(allpoleya60[p].split(':')[0].split('.')[0:brnum]):
                        alltpole6.append(allpoleya60[p])
                allpuma6.append(alltpole6)
            # allpuma6.append(alltpole6)

        print('tpole6=', tpole6)
        print('allpuma6=', allpuma6)

        allsix = []

        print('allpuma6=', allpuma6)
        # ------------------

        for k in range(len(allpuma6)):
            polessix = sorted(allpuma6[k],
                              key=lambda s: int((s.split(':')[0].split('.')[brnum]).split('^')[0].split('&')[-1]))
            allsix.append(polessix)

        print('allsix=', allsix)

        fhpole10 = []
        fhpole11 = []
        fhpole12 = []

        for i in range(len(allsix)):

            # h0 = [0]
            h60 = [0]

            for r in range(len(allsix[i])):
                # if len(allslave[i]) > 1:
                if 1:
                    h60.append(int(allsix[i][r].split(':')[0].split('.')[brnum].split('^')[0].split('&')[-1]))

            polesh60 = virtual_poles(h60, zoo=2.0, shrin=2.0, kmody=1.5, k=5)  # print('h0=', h0)
            fhpole10.append([allsix[i], h60[1:]])

            for d in range(len(allsix[i])):
                if allsix[i][d]:
                    fhpole11.append([cgstring(allsix[i][d], polesh60[d], brnum), polesh60[d]])
                    fhpole12.append(cgstring(allsix[i][d], polesh60[d], brnum))

        print('fhpole11=', fhpole11)
        print('fhpole12=', fhpole12)

        cond = sqlite3.connect("fault.db3")
        cud = cond.cursor()

        for i in range(len(fhpole12)):
            # cud.execute("update transz  set latitude =(?) where tnumber =(?) and lname =(?)" , [hpole5[i].split(':')[0].split('.')[0], poleallnum[i].split(':')[-1], str(lname)])

            cud.execute("update transz  set mpolepath =(?) where tnumber =(?) and lname =(?)",
                        [fhpole12[i].split(':')[0], fhpole12[i].split(':')[-1], str(lname)])

            cond.commit()

        cond.close()

        return fhpole12

    # branchnum为支线最大数
    # -----------------七级以上开始（全部级别解决）-----------
    for num in range(6, branchnum, 1):
        nextpole = one_line(beautypoles, num)
        beautypoles = nextpole

    # -----------------七级以上End（全部级别解决）-----------

    return True


class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, )
        # self.figure = Figure(figsize=(13.2, 6.85))
        self.figure = Figure(figsize=(13.2, 7.45))
        # self.figure = Figure()
        # self.axes = self.figure.add_subplot(111)
        self.axes = self.figure.add_axes([0.01, 0.01, 0.98, 0.98])

        # self.axes = self.figure.add_subplot(111)
        # self.axes.imshow(self.data, interpolation="quadric", aspect='auto')

        # self.pnl = wx.Panel(self, wx.TOP, size=(1340, 30))
        # self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.toolbar, 0, wx.EXPAND)
        # self.sizer.Add(self.pnl, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):

        # -----------------单线图--------------------
        choice = self.FindWindowByName('choice')
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
        ky = 1.2

        for j in range(len(total)):
            if float(total[j][5].split('-')[-1]) > 10:
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
            if float(total[i][5].split('-')[-1]) > 9:
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

        def show_map(pole_path, tcapacity, trname, trnumber):

            # -----------------------------
            # 通过pole_path找到正确的杆号标注
            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            sqe = "select  polepath from transz where tnumber ='" + str(trnumber) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            z_path0 = ('0.' + fpole[0]).split('.')
            print('z_path0=', z_path0)
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

                if t > 3:
                    y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2)) / (0.867 * t + kx)
                else:
                    y[t] = y[t] - direction[t - 1] * (z[t] * ((t + 1) % 2))

                x.append(x[t])
                y.append(y[t])

            print('x=', x)
            print('y=', y)

            print('tcapacity=', t_capacity)

            self.axes.scatter(0, 0, color='r', marker='s', edgecolors='y', s=220, linewidth=1)

            self.axes.annotate("%s" % '10kV' + lname, xy=(0, 0), size=10, xytext=(-20, -25),
                               textcoords='offset points')

            self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b',
                              s=55)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
            for w in range(0, len(z_path0)):
                if '^' not in z_path0[w]:
                    self.axes.annotate("%s" % z_path0[w].replace('&', ''), xy=(x[w], y[w]), size=10,
                                       xytext=(-10, 3),
                                       textcoords='offset points')

                if '^' in z_path0[w] and float(z_path0[w].replace('&', '').split('^')[-1]) > 2:
                    self.axes.annotate("%s" % z_path0[w].replace('&', '').split('^')[0], xy=(x[w], y[w]),
                                       size=10, xytext=(-5, 3), textcoords='offset points')

                    # pass
                else:

                    if '0' not in (z_path0[w].replace('&', '').split('^')[0]):
                        self.axes.annotate("%s" % z_path0[w].replace('&', '').split('^')[0], xy=(x[w], y[w]),
                                           size=10, xytext=(-10, 3), textcoords='offset points')
                    else:
                        self.axes.annotate('', xy=(x[w], y[w]), size=10, xytext=(-10, 3),
                                           textcoords='offset points')

            self.axes.annotate("%s" % t_capacity, xy=(x[-2], y[-2]), size=10, xytext=(0, -15),
                               textcoords='offset points')

            self.axes.annotate("%s" % t_name.replace('&', ''), xy=(x[-2], y[-2]), size=10, xytext=(0, -30),
                               textcoords='offset points')

            self.axes.plot(x, y, color='black', linewidth=0.8)
            # wi.plot_text("%s" % t_name.replace('&', ''), x[-2], y[-2])
            # wi.plot(x, y, color='black', linewidth=0.8)

            return x, y

        def show_last(zbase, pole_last, cpacity_last, trname_last, trnumber_last):

            # 通过pole_path找到正确的杆号标注
            cone = sqlite3.connect("fault.db3")
            cue = cone.cursor()
            sqe = "select  polepath from transz where tnumber ='" + str(trnumber_last) + "'"
            cue.execute(sqe)
            fpole = cue.fetchone()
            print('fpole=', fpole)
            z_path9 = ('0.' + fpole[0]).split('.')
            print('z_path0=', z_path9)
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

            # plt.annotate("%s" % z_path[-1], xy=(x[-2], y[-2]), size=10, xytext=(10, 0), textcoords='offset points')

            self.axes.annotate("%s" % z_path9[-1].replace('&', ''), xy=(x[-2], y[-2]), size=10, xytext=(-18, 3),
                               textcoords='offset points')
            '''
            if z_path[-2] != '0':
                plt.annotate("%s" % z_path[-2].replace('&', ''), xy=(x[-3], y[-3]), size=10, xytext=(2, 10 * direction[-2]),
                             textcoords='offset points')
            '''
            if z_path9[-2] != '0':
                self.axes.annotate("%s" % (z_path9[-2].replace('&', '')).split('^')[0], xy=(x[-3], y[-3]), size=10,
                                   xytext=(-18, 3),
                                   textcoords='offset points')
            else:
                self.axes.annotate('', xy=(x[-3], y[-3]), size=10,
                                   xytext=(-18, 3),
                                   textcoords='offset points')
            self.axes.annotate("%s" % capa_last, xy=(x[-2], y[-2]), size=10, xytext=(8, -15),
                               textcoords='offset points')

            self.axes.annotate("%s" % tname_last, xy=(x[-2], y[-2]), size=10, xytext=(16, -30),
                               textcoords='offset points')

            # wi.plot(x, y, color='black', linewidth=0.8)
            self.axes.plot(x, y, color='black', linewidth=0.8)

            # plt.plot(x, y, color='black', linewidth=0.8)
            self.axes.scatter(x[-1], y[-1], color='b', marker='o', edgecolors='b',
                              s=55)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）

            return x, y

        # print('3^2=', '3^2'.split('^'))

        tbsxy = []
        tbexy = []

        for j in range(len(polepath)):
            print('\n')
            print('polepath[j]=', polepath[j])
            xn, yn = show_map(polepath[j], tcapa[j], tname[j], tnumber[j])
            print('xn=', xn)
            tbsxy.append([tname[j], tcapa[j], xn, yn])

            print('xn=', xn)

        xmmax = []
        ymmax = []

        for j in range(len(pole_last)):
            print('\n')
            print('pole_last[j]=', pole_last[j])
            xm, ym = show_last(polebase, pole_last[j], tcapa_last[j], tname_last[j], tnumber_last[j])
            tbsxy.append([tname_last[j], tcapa_last[j], xm, ym])
            xmmax.append(xm)
            ymmax.append(ym)

        print('tbsxy=', tbsxy)
        print('ymmax=', ymmax)

        # xm, ym = show_last(50, '0.102.19.9.9.5.5', tcapa_last, tname_last)
        self.axes.plot([0.0, int(polebase)], [0.0, 0.0], color='red')
        self.axes.plot([int(polebase), int(polebase)], [0.0, min(ymmax[-1])], color='red')
        '''
        self.axes.annotate("%s" % int(polebase), xy=(int(polebase), 0), size=10, xytext=(0, 8),
                           textcoords='offset points')
        '''
        # self.axes.title('10kV' + lname + '配网单线图' + '\n')
        # self.axes.show()

        # -----------------单线图--------------------


class DFrame(wx.Frame):
    def __init__(self, parent):
        '''
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="配网故障定位",
                          size=(1340, 820), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        '''

        wx.Frame.__init__(self, parent, title="配网自动成图", size=(1340, 820))

        ico = wx.Icon("resources/bats.ico", wx.BITMAP_TYPE_ICO)
        # 设置图标
        self.SetIcon(ico)
        self.Center()
        # create a panel in the frame
        choice = self.FindWindowByName('choice')
        choice_test = format(choice.GetValue())
        lname = choice_test

        cond = sqlite3.connect("fault.db3")
        cud = cond.cursor()
        sqm = "select  tname from transz where trim(mpolepath) != ''  and lname='" + str(lname) + "'"
        cud.execute(sqm)
        total = len(cud.fetchall())
        print('totaltransz = ', total)
        cond.commit()
        cond.close()

        if total:
            pass
        else:
            polemodify(lname)

        # pnl = wx.Panel(self, size=(1340, 820))
        pnl = wx.Panel(self)
        panel = CanvasPanel(pnl)
        panel.draw()


'''

cont = sqlite3.connect("fault.db3")
cut = cont.cursor()
sqz = "select  * from transz "
cut.execute(sqz)
transzall = cut.fetchall()
lentran = len(transzall)
print('lentran =', lentran)
cont.commit()
cont.close()

cont = sqlite3.connect("fault.db3")
cut = cont.cursor()
sqz = "select  * from transz "
cut.execute(sqz)

line_all = []

for i in range(lentran):

    line_all.append(transzall[i][6])


    cont.commit()

cont.close()



print('line_all =', line_all)

line_list = sorted(list(set(line_all)))
print('line_list =', line_list)

for k in range(len(line_list)):
    try:
        polemodify(line_list[k])
    except:
        pass

'''

# polemodify('春黄线')


# polemodify('三州线')
