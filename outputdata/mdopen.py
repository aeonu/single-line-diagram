# cython: language_level=3
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Date    : 2019-12-01 00:23:45
# @Function: 配网故障定位
# @Author  : Elenut_luoxiaochun
# @version : 1.1.3


import markdown
import webbrowser

def readme():
    """
    转化文件的格式。
    convert(source, to, format=None, extra_args=(), encoding='utf-8', outputfile=None, filters=None)
    parameter-
        source：源文件
        to：目标文件的格式，比如html、rst、md等
        format：源文件的格式，比如html、rst、md等。默认为None，则会自动检测
        encoding：指定编码集
        outputfile：目标文件，比如test.html（注意outputfile的后缀要和to一致）
    """
    try:
        import pypandoc
        return pypandoc.convert_file('issue-8.md', 'html', format='md',outputfile='1.html')
    except (IOError, ImportError):
        with open('issue-8.md') as f:
            return f.read()
readme()

webbrowser.open('issue-8.pdf')
