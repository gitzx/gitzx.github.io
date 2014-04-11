---
date: 2014-4-11 21:17:30+00:00
layout: post
title: 二叉树的构建
thread: 53
categories: algorithm
tags: algorithm
---

1.根据二叉树的前序、中序遍历构建二叉树

	{% highlight C++ %}
	struct TreeNode{
		int key;
		TreeNode *left, *right;
	}TreeNode;

	TreeNode *buildTree(int *preorder, int *inorder,int len){
		TreeNode *root=(TreeNode*)malloc(sizeof(TreeNode));
		if(len<=0)
			return NULL;
		else{
			int index=0;
	    	while(index<len && *(preorder)!=*(inorder+index)){
				index++;
			}
			root->key=*preorder;
			root->left=buildTree(preorder+1, inorder, index);
			root->right=buildTree(preorder+(index+1), inorder+(index+1),len-(index+1));
		}
			return root;
	}
	{% endhighlight %}

2.根据二叉树的中序、后序遍历构建二叉树

	{% highlight C++ %}
	struct TreeNode{
		int key;
		TreeNode *left, *right;
	}TreeNode;

	TreeNode *buildTree(int *inorder, int *postorder,int len){
		TreeNode *root=(TreeNode*)malloc(sizeof(TreeNode));
		if(len<=0)
			return NULL;
		else{
			int index=0;
	    	while(index<len && *(postorder+len-1)!=*(inorder+index)){
				index++;
			}
			root->key=*(inorder+index);
			root->left=buildTree(inorder, postorder, index);
			root->right=buildTree(inorder+(index+1), postorder+index,len-(index+1));
		}
			return root;
	}
	{% endhighlight %}
	
3.无法根据二叉树的前序、后序遍历构建二叉树。





