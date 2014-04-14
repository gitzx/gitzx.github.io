---
date: 2014-4-14 23:02:30+00:00
layout: post
title: C指针小结
thread: 55
categories: c++
tags: c++
---

 指针是指向某种类型对象的复合数据类型，保存的是该对象的地址（迭代器只能用于访问容器内的元素）；
 
 对指针进行解引用(*)操作，可以获得该指针所指对象的地址；
 
 将取址操作符(&)作用于一个对象上时，返回的是该对象的存储地址。取址操作符只能作用于左值。
 
函数的取值有三种：(1)保存一个特定对象的地址；(2)指向某个对象后面的另一个对象；(3)0值,指针保存0值，则表明它不指向任何对象。

###指针和数组###
 
	{% highlight C++ %}
	#include<iostream>
	using namespace std;
	int *p1, *p2;
	void func1(){
		int num;
		num=11;
		p1=&num;
	}
	void func2(){
		p2=new int;//动态分配
		*p2=22;
	}
	int main(){
		func1();
		//错误，p1成野指针,虽然在我的系统中输出11
		cout<<*p1<<endl;
		func2();
		cout<<*p2<<endl;//输出22
		delete p2;
		return 0;
	} 
	{% endhighlight %}
 
###常量指针和指针常量###

(1)常量指针：被指的对象是常量。例如：`const int *p;`或`int const *p;`

(2)指针常量：指针本身是常量。例如: `int * const p;`

###数组指针###

	{% highlight C++ %}
	int *p;
	p=new int[5]{1,2,3,4,5};
	{% endhighlight %}	
	
等价于：
	
	{% highlight C++ %}
	int *p;
	int num[5]={1,2,3,4,5};
	p=&num[0];或 p=num;(p=&num错误 )
	*(p+2)  //输出3
	{% endhighlight %}	
 
###函数指针###

函数指针是指向函数而非对象的指针。函数类型由其返回类型和形参表确定，与函数名无关。

函数指针只能通过同类型的函数或函数指针或0值常量表达式进行初始化或赋值。

	{% highlight C++ %}
	#include<iostream>
	using namespace std;
	void func(int *num){
		*num=*num+5;
	}
	int main(){
		int num=11;
		func(&num);
		cout<<num<<endl;
		(*func)(&num);//通过函数指针调用函数
		cout<<num<<endl;
		return 0;
	}
	{% endhighlight %}
	
####函数指针和指针函数####

(1)函数指针是指向函数而非对象的指针；

函数指针： `int (*function) (double*,char);`这个指针指向一个函数，此函数返回int型并带有两个分别是double*型和char型的形参。

(2)指针函数，就是返回指针的函数.函数的返回值不仅仅局限于指向变量的指针，也可以是指向函数的指针。例如

	{% highlight C++ %}
	char *strcat( char *dest, const char *src );
	char *strcpy( char *dest, const char *src );
	char *strchr( const char *s, int c );
	char *strstr( const char *src, const char*sub );
	{% endhighlight %}

指针函数： `int (*function(int)) (double*,char);`首先看function(int)，将function声明为一个函数，它带有一个int型的形式参数，这个函数的返回值为一个指针。

###类指针###

类指针是指向类的指针。

	{% highlight C++ %}
	#include<iostream>
	using namespace std;
	class MyClass{
	public:
		int num;
		int nchar;
	};
	int main(){
		MyClass myclass;//myclass是一个MyClass
		myclass.num=10;
		myclass.nchar='a';
		//输出10 97
		cout<<myclass.num<<" "<<myclass.nchar<<endl;

		MyClass *p;//p指向MyClass
		p=new MyClass;
		p->num=10;
		p->nchar='a';
		//输出10 97
		cout<<p->num<<" "<<p->nchar<<endl;
		delete p;
	}
	{% endhighlight %}



