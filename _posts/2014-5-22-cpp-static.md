---
date: 2014-5-22 19:26:30+00:00
layout: post
title: c++中static的使用
thread: 68
categories: c++
tags: c++
---

static是C/C++中一个关键字，用来控制变量的存储方式和可见性。（在一个程序中，内存分布包括：代码区、全局数据区、堆区、栈区）

static在C++中主要有三种使用方式：

（1）局部静态变量；

（2）外部静态变量/函数；

（3）静态数据成员/成员函数。

###局部静态变量###

和普通局部变量相比，局部静态变量的特点（“全局性”和“记忆性”）如下：

（1）作用域相同，生存期不同。普通局部变量分配在动态存储区，函数调用结束后自动释放，局部静态变量分配在静态存储区，在程序整个运行期间都不会释放。

（2）static局部变量在所处模块在初次运行时进行初始化工作，且只操作一次。

（3）若不给局部静态变量赋初值，编译期会自动赋初值0或空字符。

“记忆性”的例子如下：

	{% highlight C++ %}
	#include <iostream>
	using namespace std;
	void showstat( int curr ) {
	   static int nStatic;    
	   nStatic += curr;
	   cout << "nStatic is " << nStatic << endl;
	}
	int main() {
	   for ( int i = 0; i < 5; i++ )
	      showstat( i ); //输出0 1 3 6 10
	}
	{% endhighlight %}


普通的局部变量的存储空间分配在stack上，每次调用函数时，分配的空间都可能不一样。而static具有全局唯一性的特点，都指向同一块内存，造成“不可重入性”，因此，在多线程情况下会导致程序不安全性。

###静态全局变量/函数###

和普通全局变量相比，静态全局变量的特点如下：

（1）生存期相同，作用域不同。无论是否有static限制，全局变量的生存期都是全局的，static只是限定作用域在本模块（文件）内部。

和普通函数相比，静态函数的特点如下：

（1）静态函数的作用域仅限于本文件。

（2）静态函数不能被其他文件所用，因此其他文件可以定义相同名字的函数，不会发生冲突。

	{% highlight C++ %}
	//file1.cpp
	static int varA;
	int varB;
	extern void funA()
	{
	……
	}
	static void funB()
	{
	……
	}
	 
	//file2.cpp
	extern int varB; // 使用file1.cpp中定义的全局变量
	extern int varA; // 错误! varA是static类型, 无法在其他文件中使用
	extern vod funA(); // 使用file1.cpp中定义的函数
	extern void funB(); // 错误! 无法使用file1.cpp文件中static函数
	{% endhighlight %}

###静态数据成员/成员函数###

和普通的数据成员相比， static既不是限定作用域的, 也不是扩展生存期的作用, 而是指示变量/函数在此类中的唯一性。静态数据成员的特点如下：

（1）静态数据成员属于一个类而不是属于此类的任何特定对象。

（2）静态成员初始化与一般数据成员初始化不同。静态数据成员初始化的格式如下：`<数据类型><类名>::<静态数据成员名>=<值>`

（3）静态数据成员的初始化在类体外进行，且前面不加static。同时初始化时不加该数据成员的权限控制符如public、private等。

（4）静态数据成员是静态存储的，它是静态生存期，必须对它进行初始化。

（5）引用静态数据成员时，采用如下格式：`<类名>::<静态成员名>`
	
	{% highlight C++ %}
	#include <iostream>
	using namespace std;
	class CMyClass {
	public:
	   static int m_i;
	};
	int CMyClass::m_i = 0;
	CMyClass myObject1;
	CMyClass myObject2;
	int main() {
	   cout << myObject1.m_i << endl; //0
	   cout << myObject2.m_i << endl; //0
	
	   myObject1.m_i = 1;
	   cout << myObject1.m_i << endl; //1
	   cout << myObject2.m_i << endl; //1
	
	   myObject2.m_i = 2;
	   cout << myObject1.m_i << endl; //2
	   cout << myObject2.m_i << endl; //2
	}
	{% endhighlight %}


和普通的成员函数相比，静态成员函数的特点如下：

（1）静态成员函数属于一个类而不是此类的任何特定对象。

（2）针对静态数据成员而言, 成员函数不管是否是static, 在内存中只有一个副本, 普通成员函数调用时, 需要传入this指针, static成员函数调用时, 没有this指针. )

（3）在静态成员函数的实现中不能直接引用类中说明的非静态成员，可以引用类中说明的静态成员。如果静态成员函数中要引用非静态成员时，可通过对象来引用。

从静态成员函数访问到非静态数据成员的两种方法：

第一种声明类的所有数据成员是静态的，以便静态成员函数可以直接访问他们。例如：

	{% highlight C++ %}
	class Singleton
	{
	 public:
	  static Singleton * instance();
	private:
	  Singleton * p;
	  static Lock lock;
	};
	Singleton * Singleton::instance()
	{
	 lock.getlock(); // fine, lock is static
	 if (!p)
	  p=new Singleton;
	 lock.unlock();
	 return p;
	}
	{% endhighlight %}

另一种方法是将参照传递给需要考量的对象能够让静态的成员函数访问到对象的非静态数据。例如：

{% highlight C++ %}
class A
{
public:
  static void func(A & obj);
  intgetval() const; //non-static member function
private:
 intval;
};
//静态成员函数func()会使用参照obj来访问非静态成员val
voidA::func(A & obj)
{
  int n = obj.getval();
}
{% endhighlight %}

参考：[C++中Static作用和使用方法](http://blog.csdn.net/artechtor/article/details/2312766)   [【C/C++】static关键字的作用](http://witmax.cn/cpp-static.html)