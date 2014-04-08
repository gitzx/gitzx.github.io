---
date: 2014-4-8 21:02:30+00:00
layout: post
title: 二叉树的遍历
thread: 49
categories: algorithm
tags: algorithm
---

二叉树的遍历有两类：深度优先遍历和广度优先遍历（层次遍历）。其中，深度优先遍历分为：（1）先序遍历；（2）后序遍历；（3）中序遍历。（一般的树没有中序遍历）

###深度优先遍历###

定义二叉树的结构如下：

	{% highlight C++ %}
	struct TreeNode{
		int val;
		TreeNode *left;
		TreeNode *right;
		TreeNode(int x): val(x),left(NULL),right(Null){}
	};
	{% endhighlight %}

二叉树的先序、中序、后序遍历一般都有三种解法：（1）递归实现；（2）使用栈；（3）Morris遍历。

####递归实现####

	{% highlight C++ %}
	void TranverseBinaryTreeRecursively(TreeNode *t, TranverseOrder order)
	{
		if(t){
			if(order==pre_order) //先序遍历
				cout<< t->data <<" ";
			TranverseBinaryTreeRecursively(t->left, order);
			if(order==in_order) //中序遍历
				cout<< t->data <<" ";
			TranverseBinaryTreeRecursively(t->right, order);
			if(order==post_order) //后序遍历
				cout<< t-> data << " ";
		}
	}
	{% endhighlight %}
	
####使用栈实现####

时间复杂度为o（n），空间复杂度为o（n）。

	{% highlight C++ %}
	class Solution{
	public:
		//前序遍历
		void preorderTraversal(TreeNode *root){
			stack<const TreeNode *> s;
			const TreeNode *p=root;
			s.push(p);
			while(!s.empty()){
				p=s.top();
				s.pop();
				if(p){
					cout<< p->data <<" ";
					s.push(p->right);
					s.push(p->left);
				}
			}
			cout<<endl;
		}
		//中序遍历
		void inorderTraversal(TreeNode *root){
			stack<const TreeNode *> s;
			const TreeNode *p=root;
			while(!s.empty()||p){
				if(p){
					s.push(p);
					p=p->left;
				}else{
					p=s.top();
					s.pop();
					cout<< p->data <<" ";
					p=p->right;
				}
			}
			cout<<endl;
		}
		//后序遍历
		void postorderTraversal(TreeNode *root){
			stack<const TreeNode *> s;
			const TreeNode *p, *q;
			p=root;
			do{
				while(p){
					s.push(p);
					p=p->left;
				}
				while(!s.empty()){
					p=s.top();
					s.pop();
					//右孩子不存在或已被访问，访问之
					if(p->right==q){
						cout<< p->data <<" ";
						q=p; //保存刚访问的节点
					}else{
						//当前节点不能访问，需第二次进栈
						s.push(p);
						p=p->right;
						break;
					}
				}
			}while(!s.empty());
			cout<<endl;
		}
	}
	{% endhighlight %}

###广度优先遍历（层次遍历）###