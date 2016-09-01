---
date: 2016-8-30 18:34:30+00:00
layout: post
title: C标准库assert.h小结
thread: 151
categories: c
tags: c

---

C语言标准库有各种不同的实现，如glibc和嵌入式linux的uClibc等，不同标准库提供的函数大同小异，最基本的包括有15个头文件：

1. <assert.h>  断言

2. <ctype.h>   字符累测试

3. <errno.h>   部分库函数抛出的错误代码

4. <float.h>   浮点数运算

5. <limit.h>   检测整型数据类型值范围

6. <locale.h>  本土化

7. <math.h>    数学函数

8. <setjmp.h>   非局部跳转

9. <signal.h>   信号

10. <stdarg.h>  可变参数表

11. <stddef.h>  一些常数、变量、类型

12. <stdio.h>  输入输出

13. <stdlib.h> 常用功能库

14. <string.h>  字符串函数

15. <time.h>  时间和日期函数


### assert.h ###

头文件<assert.h>功能比较简单，唯一的目的就是提供宏assert的定义，可以在程序中使用宏来进行断言。如果断言非真（expression==0），则程序会在标准错误流输出提示信息，并使程序异常中止调用abort() 。简单例子如下：

	{% highlight C++ %}
	//#define NDEBUG
	#include <assert.h> 
	int main(int argc, char* argv[]){
	    int a = 12;
	    int b = 24;
	    assert( a > b );
	    printf("a is larger than b!");
	    return 0;
	}
	{% endhighlight %}
	
	
如果需要去掉程序中的断言，则只需要在包含头文件之前加上`#define NDEBUG`就可以。


参考：[Standard C 语言标准函数库速查](http://ganquan.info/standard-c/)



















 




















