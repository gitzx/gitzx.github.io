---
date: 2014-6-17 13:58:30+00:00
layout: post
title: linux c下makefile小结
thread: 76
categories: c++
tags: c++
---

makefile文件由一组依赖关系和规则构成。每个依赖关系由一个目标文件和一组该目标所依赖的源文件组成。规则则描述了如何通过这些依赖文件创建目标（通常目标是一个单独的可执行文件）。

make命令会读取makefile文件的内容。确定如何编译和链接这些文件，规则如下：

(1)如果这个工程没有编译过，那么我们的所有C文件都要编译并被链接;

(2)如果这个工程的某几个C文件被修改，那么我们只编译被修改的C文件，并链接目标程序;

(3)如果这个工程的头文件被改变了，那么我们需要编译引用了这几个头文件的C文件，并链接目标程序。

###gcc和g++###

cc是Unix系统的C Compiler(cc来自于昂贵的Unix系统，cc是商业软件。)，而gcc则是GNU Compiler Collection，GNU编译器套装。

gcc是C编译器；g++是C++编译器.通过扩展，gcc可以编译c++、object-c、java等。

gcc和g++的异同点如下：

(1)后缀为.c的，gcc把它当作是C程序，而g++当作是c++程序;后缀为.cpp的，两者都会认为是C++程序。

(2)编译可以用gcc/g++，而链接可以用g++或者gcc -lstdc++。因为gcc命令不能自动和C++程序使用的库联接，所以通常使用g++来完成联接。但在编译阶段，g++会自动调用gcc，二者等价。

g++常用命令如下：

(1)预处理。命令：`g++ -E test.cpp > test.i`.该命令默认不生成文件，需要重新定向。（linux下以.i后缀作为预处理后的文件）

(2)转换成汇编语言，生成.s后缀的汇编文件。命令：`g++ -S test.cpp`。

(3)生成目标代码文件。命令：`g++ -c test.cpp`。

(4)连接目标代码，生成可执行文件。命令：`g++ test.o -o test`。

也可以直接从源文件生成可执行文件。命令：`g++ test.cpp -o test`。

###makefile文件###
	
以下面的例子为例，包含有main.cpp、test1.cpp和test2.cpp三个源文件和三个空的头文件。
	
	{% highlight C++ %}
	//main.cpp
	#include<iostream>
	#include "a.h"
	using namespace std;
	extern void test1();
	extern void test2();
	int main(){
		test1();
		test2();
		cout<<"hello main()"<<endl;
		return 0;
	}

	//test1.cpp
	#include<iostream>
	#include "a.h"
	#include "b.h"
	using namespace std;
	void test1(){
		cout<<"hello test1()"<<endl;
	}

	//test2.cpp
	#include<iostream>
	#include "b.h"
	#include "c.h"
	using namespace std;
	void test2(){
		cout<<"hello test2()"<<endl;
	}
	
	//三个空的头文件
	//a.h
	//b.h
	//c.h
	{% endhighlight %}


根据上面的代码，Makefile文件如下：

	{% highlight C++ %}
	myapp: main.o test1.o test2.o
		g++ -o myapp main.o test1.o test2.o 

	main.o: main.cpp a.h
		g++ -c main.cpp

	test1.o: test1.cpp a.h b.h
		g++ -c test1.cpp

	test2.o: test2.cpp b.h c.h
		g++ -c test2.cpp

	clean: 
		-rm main.o test1.o test2.o
	{% endhighlight %}

运行输出结果如下：

	$ make
	g++ -c main.cpp
	g++ -c test1.cpp
	g++ -c test2.cpp
	g++ -o myapp main.o test1.o test2.o 
	$./myapp
	hello test1()
	hello test2()
	hello main()
	$make clean
	rm main.o test1.o test2.o
	
在make clean命令中，rm命令以减号`-`开头，减号的含义是让make命令忽略rm命令的执行结果,即不会存在目标文件不存在而导致rm命令返回错误；`clean:` 的后面为空，因此该目标总被认为是过时的，该规则总能被执行。

###make命令的选项参数###

make命令常用的三个选项如下：

(1)-k ：用于让make命令在发现错误时仍然继续运行，主要用于在一次操作中发现所有未编译成功的源文件。

(2)-n :让make命令输出将要执行的操作步骤，而不真正的执行这次操作；

(3)-f <filename> :主要用于高数make命令将哪个文件作为makefile文件。缺省情况下，make会在当前目录下寻找makefile文件或Makefile文件。

###makefile的注释和宏###

makefile的注释和c类似，以#号开头，一直到该行结尾。

在Makefile中，可以通过`MACRONAME=value`来定义宏，引用宏则使用$(MACRONAME).例如,可以将上面的g++编译器定义成宏，方便在各个系统下更改：

	#which compiler
	CC = g++

	myapp: main.o test1.o test2.o
		$(CC) -o myapp main.o test1.o test2.o 

	main.o: main.cpp a.h
		$(CC) -c main.cpp

	test1.o: test1.cpp a.h b.h
		$(CC) -c test1.cpp

	test2.o: test2.cpp b.h c.h
		$(CC) -c test2.cpp

	clean: 
		-rm main.o test1.o test2.o

其中，CC一般是makefile里面的宏定义。

参考：[cc、gcc、g++、CC的区别概括](http://blog.csdn.net/abc78400123/article/details/6827751)