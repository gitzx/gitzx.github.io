---
date: 2014-4-7 14:02:30+00:00
layout: post
title: c++ STL之迭代器iterator
thread: 47
categories: c++
tags: c++
---

STL是C++标准程序库的核心，是一个泛型的程序库。在C++标准中，STL被组织为下面的13个头文件；STL可分为容器(containers)、迭代器(iterators)、空间配置器(allocator)、配接器(adaptors)、算法(algorithms)、仿函数(functors)六个部分。

迭代器是一种"能够遍历某个序列内所有元素"的对象。  在C++标准中，迭代器部分主要由头文件< utility >,< iterator >和< memory >组成。

###迭代器的分类###

(1) Input迭代器（向前读取） ： istream

(2) Output迭代器（向前写入） ： ostream、inserter

(3) Forward迭代器（向前读取和写入） 

(4) Bidirectional双向迭代器（向前和向后读取和写入） ： list、set、multiset、map、multimap

(5) Random access随机迭代器（随机存取，可读取和写入） ： vector、deque、string、array

###迭代器的基本操作###

所有的迭代器都具有Output迭代器的操作。

####Output迭代器的操作####

(1)*iter : 迭代器所指向的实际元素；

(2)++iter (iter++) : 向前步进；

(3)TYPE() 或 TYPE(iter) : 复制迭代器（copy构造函数）

注：Output迭代器没有比较操作；因此无法检查是否到达序列尾端。

####Input迭代器增加的操作###

(1)iter1 == iter2 (iter1 != iter2) : 判断两迭代器是否指向同一位置；

####Forward前向迭代器增加的操作####

Forward迭代器是Input迭代器和Output迭代器的结合，相比Output迭代器，增加的操作有：

(1)iter1 == iter2 (iter1 != iter2) : 判断两迭代器是否指向同一位置；

(2)iter1 = iter2 : 赋值。

####Bidirectional双向迭代器增加的操作####

Bidirectional迭代器在Forward迭代器的基础上增加了回头遍历的功能。相比Output迭代器，增加的操作有：

(1)iter1 == iter2 (iter1 != iter2) : 判断两迭代器是否指向同一位置；

(2)iter1 = iter2 : 赋值。

(3)--iter (iter--) : 步退。

####Random access迭代器增加的操作####

Random access迭代器在Bidirectional迭代器的基础上增加了随机存取的能力。相比Bidirectional迭代器，增加的操作有：

(1)iter[n] : 存取位置为n的元素；

(2)iter+=n (iter-=n) : 向前（后）跳n个元素；

(3)iter+n (iter-n) : 跳向iter之后（之前）的第n个元素；

(4)iter1-iter2 : 传回iter1和iter2之间的距离；

(5)iter1<iter2 (iter1>iter2; iter1<=iter2; iter1>=iter2) : 判断iter1是否在iter2之前之后或同一位置。

###迭代器的三个辅助函数###

STL迭代器有三个辅助函数：

(1)void advance(Iterator& pos, Dist n) : 向前（向后）多个元素,没有返回值；

(2)Diat distance(Iterator& pos1, Iterator& pos2) :  处理迭代器之间的距离；

(3)void iter_swap(Iterator& pos1, Iterator& pos2) : 交换两迭代器所指的内容。

advance()和distance()提供了只有Random access迭代器才有的能力。

对于Random access迭代器，advance()和distance()函数调用pos＋＝n和pos2-pos1，因此具有常量复杂度；对于非Random access迭代器，调用n次++pos，具有线性复杂度。

	{% highlight C++ %}
	
	#include<iostream>
	#include<list>
	#include<algorithm>
	using namespace std;
	int main(){
		list<int> coll;
		for(int i=0;i<6;++i){
			coll.push_back(i);
		}
		list<int>::iterator pos=coll.begin();
		cout<<*pos<<endl;  //输出0；
		advance(pos,3);
		cout<<*pos<<endl;  //输出3；
		cout<<distance(coll.begin(), pos)<<endl;  //输出距离3；
		iter_swap(coll.begin(), --coll.end());
		for(pos=coll.begin(); pos!=coll.end(); ++pos){
			cout<<*pos<<" ";
		}  //输出5 1 2 3 4 0
		return 0;
	}
	
	{% endhighlight %}

###迭代器配接器###

STL迭代器有三种迭代器配接器：

(1)Reverse(逆向)迭代器 : 所有的标准容器都允许使用Reverse迭代器来遍历元素；容器的成员函数rbegin()和rend()各传回一个Reverse迭代器。

(2)Insert(安插)迭代器 ： 所有的Insert迭代器都属于Output迭代器类型；因此只提供赋值的能力。

(3)stream(流)迭代器  :  把stream当成算法的原点和终点；一个istream迭代器可用来从input stream中读取元素；一个ostream迭代器可用来对output stream写入元素。

####Insert迭代器的种类####

(1)back_insert_iterator  : （函数） back_inserter(cont)

(2)front_insert_iterator :  (函数) front_inserter(cont)

(3)insert_iterator : (函数) inserter(cont, pos)

	{% highlight C++ %}
	
	#include<iostream>
	#include<list>
	#include<algorithm>
	using namespace std;
	int main(){
		list<int> coll;
		for(int i=0;i<6;++i){
			coll.push_back(i);
		}
		back_insert_iterator< list<int> > back_iter(coll);
		back_inserter(coll)=55;
		list<int>::iterator pos;
		for(pos=coll.begin();pos!=coll.end();++pos){
			cout<<*pos<<" ";
		} //输出0 1 2 3 4 5 55
		cout<<endl;
		front_insert_iterator< list<int> >front_iter(coll);
		front_inserter(coll)=11;
		for(pos=coll.begin();pos!=coll.end();++pos){
			cout<<*pos<<" ";
		} //输出11 0 1 2 3 4 5 55
		cout<<endl;
		insert_iterator< list<int> > iter(coll, coll.begin());
		inserter(coll, coll.end())=66;
		for(pos=coll.begin();pos!=coll.end();++pos){
			cout<<*pos<<" ";
		} //输出11 0 1 2 3 4 5 55 66
		cout<<endl;
		return 0;
	}
	
	{% endhighlight %}





