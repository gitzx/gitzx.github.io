---
date: 2014-4-10 17:49:30+00:00
layout: post
title: 有序数组或链表转换为二叉搜索树
thread: 52
categories: algorithm
tags: algorithm
---

(1)给定一有序上升数组，构建一个最小高度的二叉搜索树。

	{% highlight C++ %}
	
	#include <iostream>
	#include <cstring>
	#include <cmath>
	using namespace std;

	const int maxn = 100;
	struct Node{
		int key;
   	 Node *lchild, *rchild, *parent;
	};
	Node *p, node[maxn];
	int cnt;

	void init(){
		p = NULL;
		memset(node, '\0', sizeof(node));
		cnt = 0;
	}
	void create_minimal_tree(Node* &head, Node *parent, 
		int a[], int start, int end){
		if(start <= end){
        	int mid = (start + end)>>1;
        	node[cnt].key = a[mid];
        	node[cnt].parent = parent;
        	head = &node[cnt++];
        	create_minimal_tree(head->lchild, head, a, start, mid-1);
        	create_minimal_tree(head->rchild, head, a, mid+1, end);
    	}
	}
	int height(Node *head){
    	if(head == NULL) return 0;
        	return max(height(head->lchild), height(head->rchild)) + 1;
	}
	void travelTree(Node *head){
    	if(head!=NULL){
        	travelTree(head->lchild);
        	cout<<head->key<<" ";
        	travelTree(head->rchild);
    	}
	}
	int main(){
		init();
    	int a[] = {0, 1, 2, 3, 4, 5, 6, 7, 8};
    	Node *head = NULL;
    	create_minimal_tree(head, NULL, a, 0, 8);
    	cout<<height(head)<<endl; //输出4
    	travelTree(head);  //输出0 1 2 3 4 5 6 7 8
    	return 0;
	}
	{% endhighlight %}

