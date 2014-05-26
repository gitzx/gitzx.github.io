---
date: 2014-5-26 12:00:30+00:00
layout: post
title: c++中const、mutable和volatile的使用
thread: 72
categories: c++
tags: c++
---

const、volatile和mutable是C++中常用的类型限定符，在这小结下.

###const的用法###

（1）const修饰普通变量和指针

	{% highlight C++ %}
	const TYPE value;
	TYPE const value;
	{% endhighlight %}

对于非指针类型的TYPE，两中写法含义一样：const修饰的类型为TYPE的变量value是不可变的。

对于指针类型的TYPE，两种表示不同含义：

- 指针本身是常量不可变：(char*) const pContent;
- 指针所指向的内容是常量不可变：const (char) *pContent;
或(char) const *pContent;

（2）const修饰函数参数

参数const通常用于参数为指针或引用的情况，若输入参数采用“值传递”方式，由于函数将自动产生临时变量用于复制该参数，该参数本就不需要保护，所以不用const修饰。
	
	{% highlight C++ %}
	//值传递方式，const无意义
	void function(const int var);
	//参数指针本身不可变，无意义（var也是通过值传递赋值）
	void function(char* const var);
	//参数指针所指内容为常量不可变
	void function(const char* var);
	//引用参数在函数内不可边
	void function(const Class& var);
	{% endhighlight %}

（3）const修饰类对象/对象指针/对象引用

const修饰类对象表示该对象为常量对象，其中的任何成员都不能被修改。对于对象指针和对象引用也是一样。

const修饰的对象，该对象的任何非const成员函数都不能被调用，因为任何非const成员函数会有修改成员变量的企图。

	{% highlight C++ %}
	class AAA
	{
		void func1();
		void func2() const;
	}
	const AAA aaa;
	aaa.func1(); //错误
	aaa.func2(); //正确
	
	const AAA* aa=new AAA();
	aa->func1(); //错误
	aa->func2(); //正确
	{% endhighlight %}

（4）const修饰数据成员

const数据成员只在某个对象生存期内是常量，而对于整个类而言却是可变的。因为类可以创建多个对象，不同的对象其const数据成员的值可以不同。所以不能在类声明中初始化const数据成员，因为类的对象未被创建时，编译器不知道const 数据成员的值是什么。例如:

	{% highlight C++ %}
	class AAA{
		const int size=100; //错误
		int array[size]; //未定义
	}
	{% endhighlight %}

const数据成员的初始化只能在类的构造函数的初始化列表中进行。要想建立在整个类中都恒定的常量，可以用类中的枚举常量来实现，例如：

	{% highlight C++ %}
	class AAA{
		enum {size1=100;size2=200;}
		int array1[size1];
		int array2[size2]; 
	}
	{% endhighlight %}

枚举常量不会占用对象的存储空间，他们在编译时被全部求值。但是枚举常量的隐含数据类型是整数，其最大值有限，且不能表示浮点数。

（5）const修饰成员函数

const修饰类的成员函数，用const修饰的成员函数不能改变对象的成员变量,也不能调用非const成员函数。一般把const写在成员函数的最后：

	{% highlight C++ %}
	class AAA{
		void func() const; 
	}
	{% endhighlight %}

对于const类对象/指针/引用，只能调用类的const成员函数。

（6）const修饰成员函数的返回值

- 一般情况下，函数的返回值为某个对象时，如果将其声明为const时，多用于操作符的重载。如果返回const对象，或返回const对象的引用，则返回值具有const属性，返回实例只能访问类A中的公有（保护）数据成员和const成员函数，并且不允许对其进行赋值操作，这在一般情况下很少用到。

- 如果给采用“指针传递”方式的函数返回值加const修饰，那么函数返回值（即指针所指的内容）不能被修改，该返回值只能被赋给加const 修饰的同类型指针：

		{% highlight C++ %}
		const char* GetString();
		char* str=GetString(); //编译错误
		const char* str=GetString(); //正确
		{% endhighlight %}

- 函数返回值采用“引用传递”的场合不多，这种方式一般只出现在类的赙值函数中，目的是为了实现链式表达。若赋值函数的返回值加const修饰，那么该返回值的内容不允许修改。如：

		{% highlight C++ %}
		class A{
			A &operate=(const A &other);
		}
		A a,b,c; //a,b,c为A的对象
		a=b=c; //正确
		(a=b)=c; //不正常，但合法
		{% endhighlight %}

（7）const常量和define宏定义的区别

- 编译器处理方式不同: define宏是在预处理阶段展开；const常量是在编译运行阶段使用。

- 类型和安全检查不同：define宏没有类型，不做任何类型检查，仅仅展开；const常量有具体的类型，在编译阶段会执行类型检查。

- 存储方式不同：define宏仅仅是展开，有多少地方使用，就展开多少次，不会分配内存；const常量会在内存中分配内存（堆中或栈中）。

###mutable的使用###

mutable是“可变的，易变的”，跟const是反义的。在C++中，mutable只能修饰类的非静态数据成员，被mutable修饰的变量永远处于可变的状态(即使在一个const函数中)，它是为了突破const的限制而设置的。

	{% highlight C++ %}
	class ClxTest
	{
	　public:
	　　ClxTest();
	　　~ClxTest();	 
	　　void Output() const;
	　　int GetOutputTimes() const;	
 
	　private:
	　　mutable int m_iTimes;
	};	 
	ClxTest::ClxTest()
	{
	　m_iTimes = 0;
	}	 
	ClxTest::~ClxTest()
	{}	 
	void ClxTest::Output() const
	{
	　cout << "Output for test!" << endl;
	　m_iTimes++;
	}	 
	int ClxTest::GetOutputTimes() const
	{
	　return m_iTimes;
	}	 
	void OutputTest(const ClxTest& lx)
	{
	　cout << lx.GetOutputTimes() << endl;
	　lx.Output();
	　cout << lx.GetOutputTimes() << endl;
	}
	{% endhighlight %}

在const成员函数Output里面是不能修改该变量的值的，用mutalbe来修饰这个变量，output就可以修改该变量的值。

###volatile###

volatile是“易变的”，用它声明的类型变量表示可以被某些编译器未知的因素更改，比如操作系统、硬件或者其它线程等。遇到这个关键字声明的变量，编译器对访问该变量的代码就不再进行优化，从而可以提供对特殊地址的稳定访问。

	{% highlight C++ %}
	#include <stdio.h>
	void main()
	{
		int i=10;
		int a = i;	 
		printf("i= %d/n",a);
		//下面汇编语句的作用就是改变内存中i的值，但是又不让编译器知道
		__asm {
	  		mov dword ptr [ebp-4], 20h
		}	 
		int b = i;
		printf("i= %d/n",b);
	}
	{% endhighlight %}

在调试版本模式运行程序(一般调试模式没有进行代码优化)，输出结果如下：i=10 i=32

在release版本模式运行程序，输出结果如下：i=10 i=10

当使用volatile 声明的变量的值的时候，系统总是重新从它所在的内存读取数据，即使它前面的指令刚刚从该处读取过数据。而且读取的数据立刻被寄存。例如：

若使用volatile修饰变量i时(`volatile int i=10;`),在调试版本和release版本的输出均是： i=10 i=32

volatile的主要用处：

（1）并行设备的硬件寄存器（如：状态寄存器）

（2）一个中断服务子程序中会访问到的非自动变量(Non-automatic variables)

（3）多线程应用中被几个任务共享的变量

一个参数既可以是const还可以是volatile：一个例子是只读的状态寄存器。它是volatile因为它可能被意想不到地改变。它是const因为程序不应该试图去修改它。

###mutable和volatile的区别###

对于mutable，编译器能知道一个mutable变量发生改变；

对于volatile，编译器无法指定一个volatile的变量发生改变。

参考：[C++中const、volatile、mutable的用法](http://blog.csdn.net/wuliming_sc/article/details/3717017) [volatile vs. mutable in C++](http://stackoverflow.com/questions/2444695/volatile-vs-mutable-in-c)

