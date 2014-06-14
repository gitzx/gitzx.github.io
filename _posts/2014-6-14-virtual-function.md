---
date: 2014-6-14 11:19:30+00:00
layout: post
title: c++虚函数小结
thread: 74
categories: c++
tags: c++
---

在C++中，通过基类的引用或指针调用虚函数时，发生动态绑定。引用（或指针）既可以指向基类对象也可以指向派生类对象。用引用（或指针）调用的虚函数在运行时确定，被调用的函数是引用（或指针）所指对象的实际类型所定义。

###虚函数###

C++中的调用函数默认不使用动态绑定。要触发动态绑定，必须满足两个条件：

(1)只有指定为虚函数的成员函数才能进行动态绑定，非虚函数不能进行动态绑定；

(2)必须通过基类类型的引用或指针进行函数调用。
	
非虚函数在编译时根据该函数的对象、引用或指针的类型确定。

覆盖虚函数机制：

使用作用域操作符可以覆盖虚函数机制并强制使用函数调用使用虚函数的特定版本。

	{% highlight C++ %}
	Item_base *basep = &derived;
	double d=basep->Item_base::net_price(42);
	{% endhighlight %}

###虚函数表###

虚函数是通过一张虚函数表来实现（简称V-Table）。虚函数表主要是一个类的虚函数的地址表，这张表解决了继承、覆盖的问题，保证其容真实反应实际的函数。

	{% highlight C++ %}
	 class Base {
     public:
     	virtual void f() {cout << "Base::f" << endl;}
        virtual void g() {cout << "Base::g" << endl;}
        virtual void h() {cout << "Base::h" << endl;}
 
	};
	typedef void(*Fun)(void);
	Base b;
	Fun pFun=NULL;
	//虚函数表地址：0012FED4
	cout<<"虚函数表地址："<<(int*)(&b)<<endl;
	//虚函数表第一个函数地址：0044F148
	cout<<"虚函数表第一个函数地址："<<(int*)(int*)(&b)<<endl;
	pFun=(Fun)*((int*)*(int*)(&b));
	//输出Base::f
	pFun();
	{% endhighlight %}

###基类和派生类之间的转换###

(1)派生类到基类的转换（引用转换不同于对象转换）

将派生类的对象传给希望接受基类引用的函数，实际上实参是派生类型对象的引用，对象本身未被复制；

讲派生类对象传给希望接受基类类型对象的函数时，则该派生类对象的基类部分被复制到形参。

(2)从基类到派生类的自动转换是不存在的，需要派生类对象时不能使用基类对象。

若知道从基类到派生类的转换是安全的，可以使用强制转换（static_cast、dynamic_cast）。

###纯虚函数###

将函数定义为纯虚函数，则该函数为后代类型提供了可以覆盖的接口，但基类中的版本不会被调用。

含有（或继承）一个或多个纯虚函数的类是抽象基类。除了作为抽象基类的派生类的对象的组成部分，不能创建抽象类型的对象。

在函数的形参表后面写上`=0`以指定纯虚函数：

	{% highlight C++ %}
	class Disc_item:public Item_base{
	public:
		double net_price(std::size_t) const =0;
	}
	{% endhighlight %}
	

参考：[C++ 虚函数表解析](http://blog.csdn.net/haoel/article/details/1948051/)



