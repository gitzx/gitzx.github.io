---
date: 2014-5-11 19:22:30+00:00
layout: post
title: c++ stl之仿函数(functor)
thread: 67
categories: c++
tags: c++
---

仿函数(functor)是STL的六大组件之一。仿函数是一个“行为类似函数”的对象，并在类中定义了operator(),因此，我们可以在仿函数的对象后面加上一个小括号，以此调用仿函数所定义的operator().

###仿函数和一般函数比较###

一般函数的写法：

	{% highlight C++ %}
	void func(){
		statements
	}
	{% endhighlight %}

仿函数的写法：

	{% highlight C++ %}
	class FunctionObjectType{
	public:
		void operator(){
			statements;
		}
	};
	{% endhighlight %}
	
仿函数和一般函数的比较：

(1)仿函数可以同时拥有两个状态不同的实体(instance),而一般函数则没有；

(2)每个仿函数都有其型别（仿函数的型别主要用来表现函数参数型别和传回值型别）。因此可以将仿函数的型别当作template参数来传递，从而指定某种行为模式。同时容器型别也会因仿函数的不同而不同；

(3)在执行速度上，仿函数通常比函数指针快。


###STL仿函数和STL算法的关系###

	{% highlight C++ %}
	template <typename T>
	class functor{
		void operator()(...);
	};
	
	//functorobj为stl内建的仿函数,
	//或用户自定义的仿函数。
	algorithm(first,last,...,functorobj){
		functorobj(...);
	}
	{% endhighlight %}

###STL仿函数的分类###

- 按operator操作数的个数划分，可分为一元和二元仿函数；

- 按功能来划分，可分为算术运算、关系运算和逻辑运算三大类。

(1)算术类仿函数(包括加、减、乘、除、模数、否定)：

	{% highlight C++ %}
	template <class T>
	struct plus: public binary_function(T,T,T){
		T operator()(const T& x, const T& y) const{
			return x+y;
		}
	};
	template <class T>
	struct minus:public binary_function(T,T,T){
		T operator()(const T& x, const T& y) const{
			return x-y;
		}
	};
	template <class T>
	struct multiplies: public binary_function(T,T,T){
		T operator()(const T& x, const T& y) const{
			return x*y;
		}
	};
	template <class T>
	struct divides:public binary_function(T,T,T){
		T operator()(const T& x, const T& y) const{
			return x/y;
		}
	};
	template <class T>
	struct modulus: public binary_function(T,T,T){
		T operator()(const T& x, const T& y) const{
			return x%y;
		}
	};
	template <class T>
	struct negate:public binary_function(T,T){
		T operator()(const T& x) const{
			return -x;
		}
	};
	{% endhighlight %}
	
仿函数的使用，例如：

	{% highlight C++ %}
	#include<iostream>
	#include<functional>
	using namespace std;
	int main(){
    	plus<int> plusobj;
    	cout<<plusobj(3,5)<<endl; //8
    	//直接使用仿函数的临时对象
    	cout<<plus<int>()(3,5)<<endl; //8
	}

	//搭配STL算法使用
	accumulate(iv.begin(),iv.end(),plus<int>());
	{% endhighlight %}
	
(2)关系运算类仿函数

STL内建的关系运算类仿函数包括等于(equal_to)、不等于(not_equal_to)、大于(greater)、大于等于(greater_equal)、小于(less)、小于等于(less_equal)。

例如以递增次序对vector iv进行排序：

	{% highlight C++ %}
	sort(iv.begin(), iv.end(), greater<int>());
	{% endhighlight %}

(3)逻辑运算类仿函数

	{% highlight C++ %}
	template <class T>
	struct logical_and: public binary_function<T,T,bool>{
    	bool operator()(const T& x, const T& y) const{
        	return x && y;
    	}
	};
	template <class T>
	struct logical_or : public binary_function<T,T,bool>{
    	bool operator()(const T& x,const T& y) const{
        	return x || y;
    	}
	};
	template <class T>
	struct logical_not : public binary_function<T,bool>{
    	bool operator()(const T& x)const{
        	return !x;
    	}
	};
	{% endhighlight %}
	
###for_each()的回返值###

仿函数按值传递时，无法存取并改变仿函数的最终状态，改变的是仿函数的副本。有两种方法可以从“运用了仿函数”的算法中获取结果反馈：

(1)按引用传递方式传递仿函数；

(2)使用for_each()获取返回值。

以for_each()获取返回值的例子如下：

	{% highlight C++ %}
	#include<iostream>
	#include<vector>
	#include<algorithm>
	using namespace std;
	class MeanValue{
	private:
    	long num;
    	long sum;
	public:
    	MeanValue() : num(0),sum(0){}
    	void operator()(int elem){
        	num++;
        	sum+=elem;
    	}
    	double value(){
        	return static_cast<double>(sum)/static_cast<double>(num);
    	}
	};
	int main(){
    	vector<int> coll;
    	for(int i=0;i<=8;++i){
        	coll.push_back(i);
    	}
    	MeanValue mv=for_each(coll.begin(),coll.end(),MeanValue());
    	cout<<"mean value:"<<mv.value()<<endl; //4.5
	}
	{% endhighlight %}










