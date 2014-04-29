---
date: 2014-4-29 17:32:30+00:00
layout: post
title: c++ stl之deque
thread: 61
categories: c++
tags: c++
---

和vector一样，deque也是连续线性空间。主要区别如下：

(1)vector是单向开口的(对vector头部操作效率低下)，deque是双向开口的；

(2)vector是通过"重新配置一块更大空间，复制元素，再释放旧空间"来解决就空间不足； 而deque是动态地以分段连续空间组合而成，随时可以增加一段新的空间并链接起来；

(3)vector和deque都提供随机存取迭代器（Random Access Iterator），但deque的迭代器并不是普通指针，复杂度更高。因此优先选择vector。（例如对deque排序，可将deque复制到一个vector中，将vector排序（stl sort算法）后，在负责回deque）。

###deque的数据结构###

	{% highlight C++ %}
	template <class T,class Alloc=alloc,size_t BufSiz=0>
	class deque{
	public:
		typedef T value_type;
		typedef value_type* pointer;
		typedef size_t size_type;
	public:
		typedef _deque_iterator<T,T&,T*,BufSiz>
	protected:
		typedef pointer* map_pointer;
	protected:
		iterator start;
		iterator finish;
		//采用一小块连续存储空间，每个元素都是指针
		//指向各个的连续线性空间
		map_pointer map;
		size_type map_size;
	
	public:
		iterator begin(){return start;}
		iterator end(){return finish;}
		reference operator[](size_type n){
			return start[difference_type(n)];
		}
		reference front(){return *start;}
		reference back(){
			iterator tmp=finish;
			--tmp;
			return *tmp;
		}
		size_type size() const{
			return finish-start;
		}
		size_type max_size() const{
			return size_type(-1);
		}
		bool empty() const{
			return finish==start;
		}
	}
	{% endhighlight %}

###deque的元素操作###

(1)push_back

	{% highlight C++ %}
	public:
	void push_back(const value_type& t){
		if(finish.cur!=finish.last-1){
			construct(finish.cur,t);
			++finish.cur;
		}else{
			//最后缓冲区已无（或只剩一个）元素空间
			push_back_aux(t);
		}
	}
	{% endhighlight %}

(2)push_front

	{% highlight C++ %}
	public:
	void push_front(const value_type& t){
		if(start.cur!=start.first){
			construct(start.cur-1, t);
			--start.cur;
		}else{
			push_front_aux(t);
		}
	}
	{% endhighlight %}

(3)pop_front

	{% highlight C++ %}
	public:
	void pop_front(){
		if(start.cur!=start.last-1){
			destroy(start.cur);
			++start.cur;
		}else{
			pop_front_aux();
		}
	}
	{% endhighlight %}

(4)pop_back

	{% highlight C++ %}
	public:
	void pop_back(){
		if(finish.cur!=finish.first){
			--finish.cur;
			destroy(finish.cur);
		}else{
			pop_back_aux();
		}
	}
	{% endhighlight %}
