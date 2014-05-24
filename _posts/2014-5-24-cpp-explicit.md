---
date: 2014-5-24 21:10:30+00:00
layout: post
title: c++中explicit的使用
thread: 70
categories: c++
tags: c++
---

###x(y)和x=y的区别###

	{% highlight C++ %}
	//显式转换
	X x;
	Y y(x);
	//隐式转换
	X x;
	Y y=x;
	{% endhighlight %}

一个是显式转换产生了一个型别Y的新对象，一个是隐式转换产生了一个型别Y的新对象。

###explicit的作用###

在C++中，explicit关键字用来修饰类的构造函数，被修饰的构造函数的类，不能发生相应的隐式类型转换。

在C++默认情况下，只有一个参数的构造函数定义了一个隐式转换，将该构造函数对应数据类型的数据可以转换为该类对象。例如：

	{% highlight C++ %}
	class String{
		String(int n); //分配n个字节空字符串
		String(const char* p); //用C风格的字符串作为初始值
		...
	}
	//显示转换
	String s1(10); ok,分配10个字节空字符串
	String s2("hello"); //ok
	//隐式转换
	String s3=10; //ok,分配10个字节空字符串
	String s4="hello" //ok
	{% endhighlight %}

在上面例子中，“隐式转换”会int类型和char类型转换为字符串类型，容易引起误解。

利用关键字explicit 可以有效得防止构造函数的隐式转换带来的错误或者误解。例如：

	{% highlight C++ %}
	class String{
		explicit String(int n); //分配n个字节空字符串
		explicit String(const char* p); //用C风格的字符串作为初始值
		...
	}
	//显示转换
	String s1(10); ok,分配10个字节空字符串
	String s2("hello"); //ok
	//隐式转换
	String s3=10; //编译错误
	String s4="hello" //编译错误
	{% endhighlight %}
		