---
date: 2016-9-11 19:02:30+00:00
layout: post
title: C标准库errno.h/locale.h/setjmp.h/signal.h小结
thread: 158
categories: c
tags: c

---

这篇小结下errno.h/locale.h/setjmp.h/signal.h这个四个头文件。


### errno.h ###

errno.h定义了通关错误码来返回错误信息的宏。

定义的宏有：	

1. errno宏定义为一个int型的左值，包含任何函数使用errno功能所产生的上一个错误码。

其他表示错误码，定义为整数值的宏：

1. EDOM ： 源自于函数的参数超出范围，如sqrt(-1)

2. ERANGE ： 源自于函数的结果超出范围

3. EILSEQ ： 源自于不合法的字符顺序。

简单例子：

	{% highlight C++ %}
	＃include<errno.h>
	#include<math.h>
	void f(int x)
	{
		errno = 0;
		int y = sqrt(x);
		if(errno != 0)
		{
			printf("invalid x: %e\n", x);
		}
	}
	{% endhighlight %}
	
	
### locale.h ###

locale.h头文件定义了两个区域设置相关的函数和一些宏。

两个函数：

1. char *setlocale(int category, const char *locale) : 设置或恢复本地化信息

2. struct lconv *localeconv(void) : 返回当前地域设置的信息

一个变量和宏：

1. constant : 必要参数，指定设置的场景信息

2. LC_ALL ： 所有下属的常量

3. LC_COLLATE ： 排列顺序

4. LC_CTYPE ： 字符分类和转换

5. LC_MESSAGES ： 系统信息格式

6. LC_MONEYTARY ： 货币或通货格式

7. LC_NUMERIC ： 数值格式

8. LC_TIME ： 日期和时间格式

9. location ： 必要参数，指定需要进行场景信息设置的国家或区域


### setjmp.h ###

C语言不允许函数的嵌套定义，不能在一个函数内部定义另一个函数。setjmp.h头文件实现非本地控制转移，在该头文件中定义了一种特别的函数调用和函数返回顺序的方式，它允许程序流程立即从一个深层嵌套的函数中返回。	

setjmp.h声明了一个类型和定义了一个宏，一个函数：

1. 类型jmp_buf ： 数组类型，适合存储恢复一个调用环境所需的信息。

2. int setjmp(jmp_buf env) : 设置跳转点，将当前程序的状态保存在evn，供longjmp使用

3. void longjmp(jmp_buf env, int val) : 跳转

直接调用setjmp时，返回值为0，这一般用于初始化（设置跳转点时）。以后再调用longjmp宏时用env变量进行跳转。程序会自动跳转到setjmp宏的返回语句处，此时setjmp的返回值为非0，由longjmp的第二个参数指定。
 
一般地，宏setjmp和longjmp是成对使用的，这样程序流程可以从一个深层嵌套的函数中返回。

简单栗子：

	{% highlight C++ %}
	#include  <stdio.h>
	#include  <setjmp.h>
	static jmp_buf buf;
	void second(void) {
	    printf("second\n");        
	    longjmp(buf,1);            
		// 跳回setjmp的调用处
		- 使得setjmp返回值为1
	}
	 void first(void) {
	    second();
	    printf("first\n");          
		// 不可能执行到此行
	}
	 int main() {   
	    if ( ! setjmp(buf) ) {
	        first();               
		// 进入此行前，setjmp返回0
	    } else {                  
		// 当longjmp跳转回，
		setjmp返回1，因此进入此行
	        printf("main\n");  
	    }
	     return 0;
	}
	{% endhighlight %}
	
	
### signal.h ###

信号是程序执行过程中发生的异常事件。同步信号的产生是因为程序自身的某些动作，例如除零或不正当的访问存储器。异步信号是由程序外部的行为引起的，如敲击键盘，或者另外一个程序异步执行给该程序法信号。

程序不能屏蔽的信号要求立即得到处理，如果不对发生的信号指定一种处理方法，那么它就会被作为一种致命错误对待，然后程序就会以失败的状态终止执行。C标准库中的signal.h头文件提供了一些函数用以处理执行过程中所产生的信号。

头文件signal.h为处理各种信号，声明了一个类型和两个函数，并定义了几个宏。

定义的类型是：

1. sig_atomic_t ： 整数类型，声明为这种类型的对象可以作为一个原子实体被访问。

定义的函数有：

1. void (*signal(int sig, void ( *func)(int))) (int)  : 指定信号处理。通过3种方式来保证接收到的信号编号sig被依次处理，如果func的值是SIG_DFL，那么就使用默认的信号处理方式，如果func的值是SIG_IGN，那么这个信号就会被忽略，否则，func就指向一个函数，当这个信号发生时，就调用这个函数(信号处理函数)。

2. int raise(int sig) : 函数把信号sig送给正在执行的程序。执行成功返回零，否则返回非零。

定义的宏有：

以SIG_开头的宏用于定义信号处理函数

1. SIG_DFL ： 默认信号处理函数

2. SIG_ERR ： 表示一个错误信号，当signal函数调用失败时的返回值。

3. SIG_IGN ： 信号处理函数，表示忽略该信号

以SIG开头的宏用来表示一个信号代码：

1. SIGABRT ： 异常终止，比如执行了abort函数

2. SIGFPE ： 浮点错误，如除零或在导致溢出的操作

3. SIGILL ： 非法操作，如一条非法指令

4. SIGINT ： 交互式操作产生的信号，如CTRL_C

5. SIGSEGV ： 对存储器的无效访问

6. SIGTERM ： 送到程序中的终止请求


























	






















参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















