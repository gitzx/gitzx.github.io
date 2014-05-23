---
date: 2014-5-23 11:11:30+00:00
layout: post
title: c++中extern的使用
thread: 69
categories: c++
tags: c++
---

static、extern、auto、register、volatile、restrict是C/C++中常用的存储类型修饰符，上一篇小结了static的用法，这篇小结下extern的使用。

在C++中，extern主要有两个作用：

###extern声明一个变量或函数###

当extern声明一个变量或函数，指定它具有外部链接（其名称在用于定义它的文件之外的其他文件可见）。默认情况下，文件范围内的变量和函数的声明是外部的。（即下述两个函数声明没有明显的区别：
extern int f(); 和int f();）


		{% highlight C++ %}
		//test1.h
		#ifndef TEST1H
		#define TEST1H
		extern char g_str[]; //声明全局变量
		#endif
		
		//test1.cpp
		#include "test1.h"
		char g_str[]="123" //定义全局变量
		void fun1(){cout<<g_str<<endl;} //123
		
		//test2.cpp
		#include "test1.h"
		void fun2(){cout<<g_str<<endl;} //123
		{% endhighlight %}


注意：

(1)g_str是整个工程的全局变量，在内存中只存在一份。test1和test2编译链接过后，在test1.obj中可以找到“123”，在test2.obj中不存在“123”。

(2)全局变量的声明和定义不要放在一起，否则相当于没有extern修饰。例如在test1.h中定义g_str，把test1.cpp中的定义去掉，会出现连接错误。（test1.cpp和test2.cpp中都包含了“test1.h”，会都定义一次g_str,连接器会发现两个g_str）.

(3)对应（2）的解决方法（不推荐）：把`#include "test1.h"`换成`extern char g_str[]`.编译器就知道g_str是引自于外部的一个编译模块了，不会在本模块中再重复定义一个出来。

###extern与“C”一起连用###

当与“C”一起连用时，例如`extern "C" void fun();`,用于告诉编译器在编译fun时按照C的规则去编译和连接而不是C++的方式。（C++支持函数重载，编译时会对函数名进行修饰，生成一个中间的函数名称，而C不会）。例如，在C标准头文件中都有类似以下的结构：

		{% highlight C++ %}
		#ifndef __INCvxWorksh
		#define __INCvxWorksh
		#ifdef __cplusplus
		extern "C"{
			#endif
			/*...*/
			#ifdef __cplusplus
		}
		#endif
		#endif /* __INCvxWorksh*/
		{% endhighlight %}

其中：头文件中的编译宏“#ifndef __INCvxWorksh、#define __INCvxWorksh、#endif” 的作用是防止该头文件被重复引用。

（1）在C++中引用C语言中的函数和变量。
		
		{% highlight C++ %}
		/* c语言头文件：cExample.h */
		#ifndef C_EXAMPLE_H
		#define C_EXAMPLE_H
		extern int add(int x,int y);
		#endif
		/* c语言实现文件：cExample.c */
		#include "cExample.h"
		int add( int x, int y )
		{
			return x + y;
		}
		// c++实现文件，调用add：cppFile.cpp
		extern "C" 
		{
			#include "cExample.h"
		}
		int main(int argc, char* argv[])
		{
			add(2,3); 
			return 0;
		}
		{% endhighlight %}

C语言中不支持extern "C"声明，在.c文件中包含了extern "C"时会出现编译语法错误。

（2）在C中引用C++语言中的函数和变量时，C++的头文件需添加extern "C"，但是在C语言中不能直接引用声明了extern "C"的该头文件，应该仅将C文件中将C++中定义的extern "C"函数声明为extern类型。

		{% highlight C++ %}
		//C++头文件 cppExample.h
		#ifndef CPP_EXAMPLE_H
		#define CPP_EXAMPLE_H
		extern "C" int add( int x, int y );
		#endif
		//C++实现文件 cppExample.cpp
		#include "cppExample.h"
		int add( int x, int y )
		{
			return x + y;
		}
		/* C实现文件 cFile.c
		/* 这样会编译出错：#include "cExample.h" */
		extern int add( int x, int y );
		int main( int argc, char* argv[] )
		{
			add( 2, 3 ); 
			return 0;
		}
		{% endhighlight %}

参考：[C/C++中extern关键字详解](http://www.cnblogs.com/yc_sunniwell/archive/2010/07/14/1777431.html) [(转)C++中extern “C”含义深层探索](http://www.cppblog.com/macaulish/archive/2008/06/17/53689.html) [使用 extern 指定链接](http://msdn.microsoft.com/zh-cn/library/0603949d.aspx)