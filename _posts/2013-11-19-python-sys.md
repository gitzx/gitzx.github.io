---
date: 2013-11-19 19:36:30+00:00
layout: post
title: python sys模块
thread: 03
categories: python
tags:  python
---

###python sys常用函数：###

	sys.argv           命令行参数List，第一个元素是程序本身路径 
	sys.modules.keys() 返回所有已经导入的模块列表 
	sys.exc_info()     获取当前正在处理的异常类,exc_type、exc_value、
	exc_traceback当前处理的异常详细信息 
	sys.exit(n)        退出程序，正常退出时exit(0) 
	sys.hexversion     获取Python解释程序的版本值，16进制格式如：0x020403F0 
	sys.version        获取Python解释程序的版本信息 
	sys.maxint         最大的Int值 
	sys.maxunicode     最大的Unicode值 
	sys.modules        返回系统导入的模块字段，key是模块名，value是模块 
	sys.path           返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值 
	sys.platform       返回操作系统平台名称 
	sys.stdout         标准输出
	sys.stdin          标准输入
	sys.stderr         错误输出
	sys.exc_clear()    用来清除当前线程所出现的当前的或最近的错误信息
	sys.exec_prefix    返回平台独立的python文件安装的位置
	sys.byteorder      本地字节规则的指示器，big-endian平台的值
	是'big',little-endian平台的值是'little'
	sys.copyright      记录python版权相关的东西
	sys.api_version    解释器的C的API版本
	sys.version_info 
	>>> sys.version_info
	(2, 4, 3, 'final', 0) 'final'表示最终,也有'candidate'表示候选，表示版本级别，是否
	有后继的发行
	sys.displayhook(value)      如果value非空，这个函数会把他输出到sys.stdout，并且将他
	保存进__builtin__._.指在python的交互式解释器里，'_'代表上次你输入得到的结果，
	hook是钩子的意思，将上次的结果钩过来
	sys.getdefaultencoding()    返回当前你所用的默认的字符编码格式
	sys.getfilesystemencoding() 返回将Unicode文件名转换成系统文件名的编码的名字
	sys.setdefaultencoding(name)用来设置当前默认的字符编码，如果name和任何一个可用的编码
	都不匹配，抛出LookupError，这个函数只会被site模块的sitecustomize	使用，一旦别
	site模块使用了，他会从sys模块移除
	sys.builtin_module_names    Python解释器导入的模块列表 
	sys.executable              Python解释程序路径 
	sys.getwindowsversion()     获取Windows的版本 
	sys.stdin.readline()        从标准输入读一行，sys.stdout.write("a") 屏幕输出a

###sys.argv###

 实现从程序外部向程序传递参数,第一个元素是程序本身路径。如test1.py脚本：

	import sys
	print sys.argv[0]
	print sys.argv[1]
	print sys.argv[2]
	print sys.argv[3]

 运行`python test.py arg1 arg2 arg3`可得

	test.py
	arg1
	arg2
	arg3

 如test2.py脚本：

	import sys,os
	os.system(sys.argv[1])
 运行`python test2.py notepad`,将打开记事本程序。

 简明python教程上的sample.py如下：

	#-*- encoding: utf-8 -*-   
	import sys
	def readfile(filename):  #从文件中读出文件内容
	    '''Print a file to the standard output.'''
	    f = file(filename)
	    while True:
	        line = f.readline()
	        if len(line) == 0:
	            break
	        print line, # notice comma  分别输出每行内容
	    f.close()
	# Script starts from here
	if len(sys.argv) < 2:
	    print 'No action specified.'
	    sys.exit()
	if sys.argv[1].startswith('--'):
	    option = sys.argv[1][2:]
	    # fetch sys.argv[1] but without the first two characters
	    if option == 'version':  #当命令行参数为-- version，显示版本号
	        print 'Version 1.2'
	    elif option == 'help':  #当命令行参数为--help时，显示相关帮助内容
	        print '''/
	This program prints files to the standard output.
	Any number of files can be specified.
	Options include:
	  --version : Prints the version number
	  --help    : Display this help'''
	    else:
	        print 'Unknown option.'
	    sys.exit()
	else:
	    for filename in sys.argv[1:]: #当参数为文件名时，传入readfile，读出其内容
	        readfile(filename)

 运行`python sample.py --version`，输出结果为：version 1.2。
 运行`python sample.py --help`，输出结果为This program prints...


###sys.platform###

 实现一个清除终端，linux下用clear, windows下用cls。

	ostype=sys.platform()
	if ostype==”linux” or ostype==”linux2”:
		Cmd=”clear”
	else:
  		Cmd=”cls”

###sys.exit(n)###

 执行至主程序的末尾时,解释器会自动退出. 但是如果需要中途退出程序, 你可以调用sys.exit 函数, 它带有一个可选的整数参数返回给调用它的程序. 这意味着你可以在主程序中捕获对sys.exit 的调用。（注：0是正常退出，其他为不正常，可抛异常事件供捕获!）

###sys.path()###

 `sys.path`可以查看已导入模块的路径。也可以利用`sys.path.append("my module pathe")`来添加自己的模块路径。