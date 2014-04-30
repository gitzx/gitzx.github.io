---
date: 2014-4-30 17:32:30+00:00
layout: post
title: c++ stl之stack
thread: 62
categories: c++
tags: c++
---

stack是STL的一个容器配接器，是一种先进后出的数据结构，只有一个出口。主要操作有新增元素、移除元素、取得最顶端元素。

stack只能操作最顶端的元素，且不提供迭代器，没有遍历功能。

配接器指的是“修改某物接口，形成另一种风貌”。使stack符合“先进后出”的容器都可以作为stack的底层结构，例如deque和list。

###以deque作为stack的底层容器###

STL以deque作为缺省情况下的stack底部结构。

	{% highlight C++ %}
	template <class T,class Sequence=deque<T> >
	class stack{
	protected:
		Sequence c;
	public:
		bool empty() const{return c.empty();}
		size_type size() const{return c.size();}
		reference top(){return c.back();}
		const_reference top() const{return c.back();}
		void push{const value_type& x}{c.push_back(x);}
		void pop(){c.pop_back();}
	}
	template <class T,class Sequence>
	bool operator==(const stack<T,Sequence>& x,const stack<T,Sequence>& y){
		return x.c==y.c;
	}
	template <class T,class Sequence>
	bool operator<(const stack<T,Sequence>& x,const stack<T,Sequence>& y){
		return x.c<y.c;
	}
	{% endhighlight %}

###以list作为stack的底层容器###

除了deque之外，list也是双向开口的数据结构，也可以利用list形成一个stack。

	{% highlight C++ %}
	#include<stack>
	#include<list>
	#include<iostream>
	#include<algorithm>
	using namespace std;
	int main(){
		stack<int, list<int> > istack;
		for(int i=0;i<5;++i){
			istack.push(i);
		}
		cout<<istack.size()<<endl; //5
		cout<<istack.top()<<endl;  //4
		istack.pop();
		cout<<istack.top()<<endl; //3
	}
	{% endhighlight %}