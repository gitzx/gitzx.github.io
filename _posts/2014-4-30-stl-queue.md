---
date: 2014-4-30 15:32:30+00:00
layout: post
title: c++ stl之queue
thread: 63
categories: c++
tags: c++
---

queue是stl的一个容器配接器，是一种先进先出的数据结构，它有两个出口。queue允许新增元素、移除元素、从最底端加入元素、取得最顶端元素。

queue出去最底端可以加入、最顶端可以取出外，不能存取其他元素，即queue不允许有遍历行为。且queue不提供迭代器。

queue的特性是“先进先出”，可以以deque和list作为底层的结构。

###以deque作为queue的底层容器###

STL使用deque作为queue缺省的底层容器。

	{% highlight C++ %}
	template <class T,class Sequence=deque<T> >
	class queue{
	protected:
		Sequence c;
	public:
		bool empty() const{return c.empty();}
		size_type size() const{return c.size();}
		reference front(){return c.front();}
		const_reference front() const{return c.front();}
		reference back(){returnn c.back();}
		const_reference back() const{return c.back();}
		void push(const value_type& x){c.push_back(x);}
		void pop(){c.pop_front();} 
	}
	template <class T,class Sequence>
	bool operator==(const queue<T,Sequence>&x, const queue<T,Sequence>& y){
		return x.c==y.c;
	}
	bool operator<(const queue<T,Sequence>7 x, const queue<T,Sequence>& y){
		return x.c<y.c;
	}
	{% endhighlight %}

###以list作为queue的底层容器###

	{% highlight C++ %}
	#include<queue>
	#include<list>
	#include<iostream>
	#include<algorithm>
	using namespace std;
	int main(){
		queue<int,list<int> > iqueue;
		for(int i=0;i<5;++i){
			iqueue.push(i);
		}
		cout<<iqueue.size()<<endl; //5
		cout<<iqueue.front()<<endl; //0
		iqueue.pop();
		cout<<iqueue.front()<<endl; //1
		cout<<iqueue.size()<<endl; //4
	}
	{% endhighlight %}