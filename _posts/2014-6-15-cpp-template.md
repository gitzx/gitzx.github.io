---
date: 2014-6-15 13:58:30+00:00
layout: post
title: c++模板小结
thread: 75
categories: c++
tags: c++
---

在C++中，模板是泛型编程的基础，模板是创建类或函数的蓝图或公式，编译器可以用它产生多种特定类型的实例。其中，函数模板是建立算法库的基础，类模板是建立标准库容器和迭代器类型的基础。

###模板的定义###

(1)函数模板的定义：

	
	template<typename/class 数据类型参数标识符>
	<返回类型><函数名>(参数表)
	{
		函数体
	}
	{% highlight C++ %}
	template <typename T>
	int compare(const T &v1, const T &v2){
		if(v1<v2) return -1;
		if(v2<v1) return 1;
		return 0;
	}
	{% endhighlight %}
	
其中，模板形参表不能为空。模板形参可以是表示类型的类型形参，也可以是表示常量表达式的非类型形参。

函数模板可以声明为inline，inline说明符放在模板形参表之后，返回类型之前。

(2)类模板的定义：

	template<typename/class 数据类型参数标识符>
	class 类名
	{
		类成员函数和成员数据
	}
	{% highlight C++ %}
	template <class Type> class Queue{
	public:
		Queue();
		Type &front();
		const Type &front() const;
		void push (const Type &);
		void pop();
	private:
		//...
	};
	{% endhighlight %}


###模板形参###

可以给模板形参赋予的唯一含义是区别形参是类型形参还是非类型形参。类型形参表示未知类型；非类型形参表示一个未知值。

(1)类型形参

类型模板形参：类型形参由关键字class或typename后接说明符构成。如`teplate<class T> void func(T t){..}`，其中T是一个类型形参。

模板类型形参可以作为类型说明符用在模板中的任何地方，与内置类型说明符或类类型说明符使用方式完全相同，可以用于指定返回类型、变量声明等。

(2)非类型形参

非类型模板形参：模板的非类型形参也就是内置类型形参。非类型模板形参只能是整型、指针和引用，像double、String、String**这样的类型是不允许的。但对象的引用或指针（double &和double *）是正确的。

非类型模板的形参在模板定义的内部是常量值。即调用非类型模板形参的实参必须是一个常量表达式；任何局部对象，局部变量，局部对象的地址，局部变量的地址都不是一个常量表达式，都不能用作非类型模板形参的实参。全局指针类型，全局变量，全局对象也不是一个常量表达式，不能用作非类型模板形参的实参。

全局变量的地址或引用，全局对象的地址或引用const类型变量是常量表达式，可以用作非类型模板形参的实参。

非类型形参一般不应用于函数模板中，比如有函数模板

	{% highlight C++ %}
	template<class T, int a> void h(T b){...}
	{% endhighlight %}
	
若使用h(2)调用会出现无法为非类型形参a推演出参数的错误，对这种模板函数可以用显示模板实参来解决，如用h<int, 3>(2)这样就把非类型形参a设置为整数3。

(3)模板形参到实参的转换

提升转换：如从short到int 的提升转换。

整值转换：如从int 到unsigned int的转换。

cosnt转换：接受const引用或const指针的函数可以分别用非const对象的引用或指针来调用，无须产生新的实例化；传递const或非const对象给接受非引用类型的函数，都使用相同的实例化。

数组或函数到指针的转换：如果模板形参不是引用类型，则对数组或函数类型的实参进行常规指针转换。

	{% highlight C++ %}
	template <typename T> T fobj(T,T);
	template<typename T> T fref(const T&,const T&);
	string s1("a value");
	const string s2("another value");
	fobj(s1,s2); //ok
	fref(s1,s2); //ok
	int a[10],b[21];
	fobj(a,b); //ok
	fref(a,b); //error
	{% endhighlight %}
	
###模板实例化###

模板在使用时将进行实例化，类模板在引用实际模板类类型时实例化；函数模板在调用它或用它对函数指针进行初始化或赋值时实例化。

	{% highlight C++ %}
	template<typename T>       
	void min(T &x, T &y)
	{  
		return (x<y)?x:y;  
	}
	int min(int,int);
	void func(int i, char j)
	{
   		min(i, i);
   		min(j, j);
   		min(i, j);
   		min(j, i);
	}
	{% endhighlight %}
	
C++中，函数模板与同名的非模板函数重载时，应遵循下列调用原则：

(1)寻找一个参数完全匹配的函数，若找到就调用它。

(2)寻找一个函数模板，若找到就将其实例化生成一个匹配的模板函数并调用它。

(3)若上面两条都失败，则使用函数重载的方法，通过类型转换产生参数匹配，若找到就调用它。

(4)若上面三条都失败，还没有找都匹配的函数，则这个调用是一个错误的调用。

参考：[C++ 模板详解（一）](http://www.cnblogs.com/gw811/archive/2012/10/25/2738929.html)



