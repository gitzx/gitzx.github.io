---
date: 2014-4-25 23:24:30+00:00
layout: post
title: c++ STL之vector
thread: 59
categories: c++
tags: c++
---

STL中vector和数组很像，唯一的差别是数组是静态空间，一旦配置了就不能改变大小；vector是动态空间，随着元素的加入，vector的内部机制会自行扩充空间。

且vectort维护的是连续线性空间，提供的是随机存取迭代器。

###vector的数据结构###

	{% highlight C++ %}
	template <class T, class Alloc=alloc>
	class vector{
	protected:
		iterator start;
		iterator finish; //目前使用空间的尾；
		iterator end_of_storage; //目前可用空间的尾；

	public:
		iterator begin(){return start;}
		iterator end() {return finish;}
		size_type size() const{
			return size_type(end()-begin());}
		size_type capacity() const{
			return size_type(end_of_storage-begin());}
		bool empty() const{
			return begin()==end();}
		reference operator[](size_type n){
			return *(begin()+n);}
		reference front(){return *begin();}
		reference back(){return *end();}
	};
	{% endhighlight %}
	
###vector的其他常用操作###

(1)vector中指定空间大小和初值的构造器

	{% highlight C++ %}
	vector(size_type n, const T& value){
		fill_initialize(n, value);
	}
	
	void fill_initialize(size_type n,const T& value){
		start=allocate_and_fill(n, value);
		finish=start+n;
		end_of_storage=finish;
	}
	iterator allocate_and_fill(size_type n, const T& x){
		iterator result=data_allocator::allocate(n);
		uninitialize_fill_n(result,n,x);
		return result;
	}
	{% endhighlight %}
	
(2)push_back()和pop_back() (vector不支持push_front())

	{% highlight C++ %}
	void push_back(const T& x){
		if(finish!=end_of_storage){
			construct(finish,x);
			++finish;
		}else{
			////vector的一个成员函数
			insert_aux(end(),x);
		}
	}

	void pop_back(){
		--finish;
		destroy(finish);
	}
	{% endhighlight %}
	
(3)resize()、erase()、clear()

	{% highlight C++ %}
	iterator erase(iterator position){
		if(position+1!=end()){
			copy(position+1,finish,position);
		}
		--finish;
		destroy(finish);
		return position;
	}

	void resize(size_type new_size, const T& x){
		if(new_size<size()){
			erase(begin()+new_size(), end());	
		}else{
			insert(end(),new_size-size(), x);
		}
	}
	void resize(size_type new_size){
		return (new_size, T());	
	}
	
	void clear(){
		erase(begin(),end());
	}
	{% endhighlight %}

