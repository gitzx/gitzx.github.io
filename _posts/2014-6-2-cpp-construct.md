---
date: 2014-6-2 10:12:30+00:00
layout: post
title: c++中构造函数的使用
thread: 73
categories: c++
tags: c++
---

构造函数是特殊的成员函数，构造函数的工作是初始化对象。只要创建类类型的对象，编译器就会运行一个构造函数。

构造函数的名字与类名字相同，且不能指定返回类型。

###构造函数的分类###

(1)无参构造函数

若一个类没有定义任何构造函数，则创建该类类型的对象时，会调用默认的无参构造函数（为所有参数都提供了默认值的构造函数）。

若一个类中已经定义了某一种构造函数，创建对象时系统就不会生成一个默认的无参构造函数，若要使用一个这样的无参构造函数，则需要自己合成一个写一个合成的默认构造函数。

(2)带参数的构造函数

一个类声明的构造函数没有数量限制，只要每个构造函数的形参表(参数个数和类型)是唯一的（构造函数可以被重载）。用于初始化一个对象的实参类型决定使用哪个构造函数。

(3)复制构造函数(拷贝构造函数)

复制构造函数具有单个形参，该形参（常用const修饰）是对该类类型的引用。

当定义一个新对象并用一个同类型的对象对它进行初始化时，将显示的使用复制构造函数；当将该类型的对象传递给函数或从函数返回该类型对象时，将隐式的使用复制构造函数。

例如：类String的结构如下

	{% highlight C++ %}
	class String{
	public:
		String(const char *str=NULL); //普通构造函数
		String(const String &other); //拷贝构造函数
		~String(void); //析构函数
		String & operator=(const String &other);//赋值函数
	private:
		char *m_data;
	};
	{% endhighlight %}

###构造函数的初始化###

构造函数除了具有一般函数的函数名、形参表和函数体外，还可以包含一个构造函数初始化列表。初始化表位于函数参数表之后，在函数体{}之前。

类的数据成员的初始化的方式有两种：

(1)构造函数初始化表。

(2)函数体内赋值。

	{% highlight C++ %}
	class A{
	public:
		A(void);
		A(int x, int y);
		A(const A &other);
	private:
		int m_x, m_y;
		int m_i, m_j;
	};
	class B{
	public:
		B(const A &a);
	private:
		A m_a;
	}
	//使用构造函数初始表初始化非内部数据类型的成员对象
	B::B(const A &a):m_a(a){}
	//使用函数体内赋值初始化非内部数据类型的成员对象
	B::B(const A &a){
		m_a=a;
	}
	//使用构造函数初始表初始化内部数据类型的数据成员
	A::A(int x, int y):m_x(x), m_y(y){
		m_i=0;
		m_j=0;
	}
	//使用函数体内赋值初始化内部数据类型的数据成员
	A::A(int x, int y){
		m_x=x;
		m_y=y;
		m_i=0;
		m_j=0;
	}
	{% endhighlight %}
	
若类存在继承关系，派生类必须在其初始化表里调用基类的构造函数

	{% highlight C++ %}
	class A{
		A(int x);
	};
	class B::public A{
		B(int x, int y);
	};
	//在初始化表中调用基类的构造函数
	B::B(int x, int y):A(x){}
	{% endhighlight %}

###“位拷贝”而非“值拷贝”###

"缺省的拷贝构造函数"和“缺省的赋值函数”均采用“位拷贝”而非“值拷贝”的方式来实现，当类中含有指针变量时，这个两个函数会出错。

例如：

	{% highlight C++ %}
	String a, b; //a、b为String的两个对象
	a.m_data="hello"; 
	b.m_data="world";
	//以下有三个错误：
	//(1)b.m_data内存没有释放，造成内存泄漏；
	//(2)b.m_data和a.m_data指向同一块内存，一个变动影响另一个
	//(3)当对象被析构时，m_data被释放两次
	b.m_data=a.m_data;  //错误
	{% endhighlight %}
	
###“深拷贝”和“浅拷贝”###

(1)浅拷贝是指在对象复制时，只对对象中的数据成员进行简单的赋值。默认的拷贝函数执行的也是浅拷贝。但一旦对象中存在动态成员，浅拷贝就会出现问题。(例如指针、静态数据成员等。)

(2)相比于浅拷贝，深拷贝对于对象中的动态成员，并不是仅仅的赋值，而是重新动态的分配空间。

	{% highlight C++ %}
	class Rect
	{
	public:
    	Rect()
    	{
        	count++; 
        	p=new int(100);
    	}
    	//拷贝构造函数
    	Rect(const Rect& r)
    	{
        	width=r.width;
        	height=r.height;
        	count++; //对象计数
        	p=new int(100); 
        	*p=*(r.p); //指针
    	}
    	~Rect()
    	{
        	count--;
    	}
    	static int getCount()
    	{
        	return count;
    	}
	private:
    	int width;
    	int height;
    	static int count;
	};
	int Rect::count=0;
	int main()
	{
    	Rect rect1;
    	Rect rect2(rect1); //深拷贝
    	return 0;
	}
	{% endhighlight %}

深拷贝与浅拷贝的区别就在于深拷贝会在堆内存中另外申请空间来储存数据，从而也就解决了指针悬挂的问题。简而言之，当数据成员中有指针时，必须要用深拷贝。




