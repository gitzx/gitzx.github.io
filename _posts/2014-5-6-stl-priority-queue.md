---
date: 2014-5-06 12:32:30+00:00
layout: post
title: c++ stl之priority_queue
thread: 64
categories: c++
tags: c++
---

和stack和queue类似，priority_queue也是stl的容器配接器。

priority_queue是一个拥有权值的queue，除了和queue一样，只允许在低端加入元素，并从顶端取出元素外，priority_queue允许用户以任何次序将任何元素推入容器，但取出时一定从优先级最高的元素开始取。

在stl缺省情况下，priority_queue利用max-heap完成。

###max-heap###

heap是一种完全二叉树（整个二叉树除了最底层的叶子节点外都是填满的，而底层叶子节点由左至右不得有空隙）。heap分为max_heap和min_heap，其中stl缺省情况下提供的是max-heap。

max-heap的最大值在根节点，总是位于底层array或vector的开头，由于array无法动态改变大小，stl缺省情况下使用vector。

(1)heap算法

heap基本算法包括

- `push_heap`：新加入的元素放在最下一层作为叶子节点，并填补由左至右的第一个空格（即把元素插入到底层vector的end()处），然后执行上移过程，即将该元素的节点拿来与其父节点比较，若其键值比父节点大，就父子对换位置，如此上移，直到不需对换或直到根节点为止。
 
- `pop_heap`：max_heap的最大值在根节点，pop操作取走根节点（vector的最后一个元素），将最下一层最右边的叶子节点拿掉。然后执行下移过程，即将该叶子节点填入根节点留下的洞，将它与其两子节点进行键值比较，并与较大子节点对换位置，直到键值大于左右两节点或直到下放到叶子节点为止。

- `sort_heap`：利用pop_heap可以获得heap中键值最大的元素，持续对heap做pop_heap操作，且每次将操作范围从后向前缩减一个元素。

- `make_heap`：将一段现有的数据转化为一个heap。

(2)max-heap实例：

	{% highlight C++ %}
	#include<vector>
	#include<iostream>
	#include<algorithm>
	using namespace std;
	int main(){
		int ia[9]={0,1,2,3,4,8,9,3,5};
		vector<int> ivec(ia,ia+9);
		make_heap(ivec.begin(),ivec.end());
		for(int i=0;i<ivec.size();++i)
			cout<<ivec[i]<<" "; //9 5 8 3 4 0 2 3 1
		cout<<end;
		ivec.push_back(7);
		push_heap(ivec.begin(),ivec.end());
		for(int i=0;i<ivec.size();++i)
			cout<<ivec[i]<<" "; //9 7 8 3 5 0 2 3 1 4
		cout<<endl;
		pop_heap(ivec.begin(),ivec.end());
		cout<<ivec.back()<<endl; //9
		ivec.pop_back();
		for(int i=0;i<ivec.size();++i)
			cout<<ivec[i]<<" "; //8 7 4 3 5 0 2 3 1
		cout<<endl;
		sort_heap(ivec.begin(),ivec.end());
		for(int i=0;i<ivec.size();++i)
			cout<<ivec[i]<<" "; //0 1 2 3 4 5 7 8 
		cout<<endl;
		return 0;
	}
	{% endhighlight %}


###priority_queue###

priority_queue的所有元素，进出都有一定规则，只有queue顶端的元素（权值最高），才有机会被取用。和heap一样，priority_queue不提供遍历功能，也不提供迭代器。

	{% highlight C++ %}
	#include<queue>
	#include<iostream>
	#include<algorithm>
	using namespace std;
	int main(){
		int ia[9]={0,1,2,3,4,8,9,3,5};
		priority_queue<int> ipq{ia,ia+9};
		cout<<ipq.size()<<endl; //9
		while(!ipq.empty()){
			cout<<ipq.top()<<" "; //9 8 5 4 3 3 2 1 0
			ipq.pop();
		}
		cout<<endl;
	}
	{% endhighlight %}