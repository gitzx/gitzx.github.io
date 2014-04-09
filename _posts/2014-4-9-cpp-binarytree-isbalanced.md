---
date: 2014-4-9 22:12:30+00:00
layout: post
title: 判断二叉树是否平衡
thread: 50
categories: algorithm
tags: algorithm
---

1. 判断一棵二叉树是否为平衡二叉树。平衡二叉树的定义是：它是一棵空树或它的左右两个子树的高度差的绝对值不超过1，并且左右两棵子树都是一棵平衡二叉树。

（1）解法一：在遍历树的每个结点的时候，调用函数TreeDepth得到它的左右子树的深度。如果每个结点的左右子树的深度相差都不超过1，按照定义它就是一棵平衡的二叉树。

	{% highlight C++ %}
	//获取二叉树的深度
	int TreeDepth(TreeNode *root){
		if(!root)
			return 0;
		int nLeft=TreeDepth(root->left);
		int nRight=TreeDepth(root->right);
		return (nLeft>nRight)? (nLeft+1):(nRight+1);
	}

	bool isBalanced(TreeNode *root){
		if(root)
			return true;
		int nLeft=TreeDepth(root->left);
		int nRight=TreeDepth(root->right);
		int diff=left-right;
		if(diff>1||diff<-1)
			return false;
		return isBalanced(root->left) && isBalanced(root->right);
	}
	{% endhighlight %}
	
 （2）解法二：直接利用递归实现，时间复杂度为o（n），空间复杂度为o（logn）
 
	{% highlight C++ %}
	int balancedHeight(TreeNode *root){
		if(root)
			return 0; //终止条件
		int nLeft=balancedHeight(root->left);
		int nRight=balancedHeight(root-right);
		if(nLeft<0||nRight<0||abs(nLeft-nRight)>1)
			return -1;
		return max(nLeft+nRight)+1;
	}

	bool isBalanced(TreeNode *root){
		return balancedHeight(root)>=0;
	}
	{% endhighlight %}
	
2. 给定一个二叉树，判断这棵树任意两个叶子结点到根结点的距离之差不大于1。（这个和判断是否为平衡二叉树有区别）


 



