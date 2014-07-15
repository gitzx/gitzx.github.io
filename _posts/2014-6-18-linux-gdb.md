---
date: 2014-6-18 11:52:30+00:00
layout: post
title: gdb使用小结
thread: 77
categories: c++
tags: c++
---

gdb是linux下调试C和C++的调试器，在这简单小结下。

###启动gdb###

在编译时，我们先要把调试信息加到可执行文件中。可以使用编译器（cc/gcc/g++）的 -g 参数。例如：`$g++ -g test.cpp -o test`

启动gdb的三种方式：

(1)`gdb test`  或分两步：`gdb`和`file test`

(2)`gdb test core` ：用gdb调试test和core文件，core是程序非法执行后core dump后产生的文件。

(3)`gdb test <pid>` :如果你的程序是一个服务程序，那么你可以指定这个服务程序运行时的进程ID。gdb会自动attach上去，并调试它。

###gdb常用命令###

在这列下常用的gdb命令：

	(1)`file [filename]` ：装入可执行文件；
	
	(2)`kill [filename]` ：终止正在调试的程序；
	
	(3)`break [file:function/line]` :在（file中）的函数或某行设置断点；
	
	(4)`clean [file:function/line]` :删除一个断点；
	
	(5)`run` :运行程序；
	
	(6)`bt 或Backtrace` : 显示程序堆栈信息；
	
	(7)`print [expr]` :打印表达式的值；
	
	(8)`continue` ：继续运行成程序；
	
	(9)`list` :列出可执行文件的源代码的一部分；
	
	(10)`next`:在断点后，单步执行，跳过函数调用；
	
	(11)`step` :在断点后，单步执行，进入函数调用；
	
	(12)`set val=0` :设置变量的值为0；
	
	(13)`watch` :监视一个变量的值而不管它何时被改变；
	
	(14)`display` :在断点停止的地方，显示指定表达式的值.
	
	(15)`finish` :继续执行，直到当前函数返回
	
	(16)`Ctrl+c` :在当前位置停止正在执行的程序，断点在当前行；
	
	(17)`return` :强制从当前函数返回；
	
	(18)`load` :动态载入一个可执行文件到调试器；
	
	(19)`shell` :在不离开gdb的情况下执行unix shell命令；
	
	(20)`make` ：在不离开gdb的情况下执行make命令；
	
	(21)`quit` :退出gdb。


 其中，上述命令可用首字母来使用，如`quit`可以使用`q`代替。其他命令可使用`help`查看。


###多线程情况###

如果程序是多线程的话，可以定义你的断点是否在所有的线程上，或是在某个特定的线程。可以使用如下命令：

`break <linespec> thread <threadno>` :linespec 指定了断点设置在的源程序的行号。threadno 指定了线程的 ID，注意，这个 ID是 GDB 分配的，你可以通过“info threads”命令来查看正在运行程序中的线程信息。

如果你不指定 thread <threadno>则表示你的断点设在所有线程上面。你还可以为某线程指定断点条件.

当程序被GDB停住时，所有的运行线程都会被停住。这方便查看运行程序的总体情况。而在恢复程序运行时，所有的线程也会被恢复运行。那怕是主进程在被单步调试时。 
