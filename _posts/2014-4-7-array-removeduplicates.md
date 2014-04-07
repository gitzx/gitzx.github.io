---
date: 2014-4-7 20:02:30+00:00
layout: post
title: 数组去重复问题
thread: 48
categories: algorithm
tags: algorithm
---

1.给定一个已排序数组，去掉重复的元素，保证每个元素只出现一次，返回新的数组和数组长度，要求时间复杂度为o（n），空间复杂度为o（1）。

	{% highlight C++ %}
	
	#include<iostream>
	#include<algorithm>
	#include<vector>
	using namespace std;
	class Solution1{
		public:
		int removeDumplicates(int A[], int n){
			return distance(A, unique(A, A+n));
		}
	};
	class Solution2{
		public:
		int removeDumplicates(int A[], int n){
			if(n==0) 
				return 0;
			int index=0;
			for(int i=1;i<n;i++){
				if(A[index]!=A[i]){
					A[++index]=A[i];
				}
			}
			return index+1;
		}
	};

	int main(){
		int A[5]={1,1,1,2,2};
		Solution1 s1;
		int d = s1.removeDumplicates(A, 5);
		for(int i=0;i<d;++i){
			cout<<A[i]<<" ";
		}  //输出1 2 
		cout<<endl;
		return 0;
	}
	
	{% endhighlight %}


2.给定一个已排序数组，去掉重复的元素，保证每个元素最多出现两次，返回新的数组和数组长度，要求时间复杂度为o（n），空间复杂度为o（1）。

	{% highlight C++ %}
	#include<iostream>
	using namespace std;
	class Solution1{
		public:
		int removeDuplicates(int A[], int n){
			if(n<=2)
				return n;
			int index=2;
			for(int i=2;i<n;++i){
				if(A[index-2]!=A[i]){
					A[index++]=A[i];
				}
			}
			return index;
		}
	};
	class Solution2{
		public:
		int removeDuplicates(int A[], int n){
			int index=0;
			for(int i=0;i<n;++i){
				if(i>0&&i<n-1&&A[i]==A[i-1]&&A[i]==A[i+1])
					continue;
				A[index++]=A[i];
			}
			return index;
		}
	};

	int main(){
		Solution1 s1; //或Solution2 s1；
		int A[8]={1,1,1,2,2,2,3,3};
		int d=s1.removeDuplicates(A, 8);
		for(int i=0;i<d;i++){
			cout<<A[i]<<" ";
		} //输出1 1 2 2 3 3
		cout<<endl;
		return 0;
	}
	
	{% endhighlight %}
	
3.在第二题的基础上，若最多允许重复3次或多次，只需稍加改动即可。例如将第二题的解法一 中2改为3或多次；将解法二中的相同项比较三次或多次。








