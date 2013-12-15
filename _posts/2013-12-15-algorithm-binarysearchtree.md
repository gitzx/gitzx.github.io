---
date: 2013-12-15 11:28:30+00:00
layout: post
title: 二叉查找树
thread: 15
categories: algorithm
tags:  algorithm
---

在这小结下二叉查找树的性质和一些基本操作。

---

- 二叉查找树须满足如下性质：

设x是二叉查找树的一个结点，若y是x左子树的一个结点，则key[x] >=  key[y]；若y是x右子树的一个结点，则key[x] <= key[y].

- 二叉查找树一些操作的运行时间：

对于一个高度为h的二叉查找树，动态集合操作 如查找、最大值、最小值、前趋和后继、插入和删除等操作的运行时间均为O（h）。

---



###三大遍历算法###

（1）中序遍历

中序遍历的顺序为：左子树的关键字--》跟的关键字 --》右子树的关键字。伪代码如下（递归方式）：

	--INORDER-TREE-WALK(x)
	if x != NIL
		then INORDER-TREE-WALK(left[x])
		print key[x]
		INORDER-TREE-WALK(right[x])

（2）前序遍历

前序遍历的顺序为：跟的关键字--》左子树的关键字--》右子树的关键字。

（3）后序遍历

后序遍历的顺序为：左子树的关键字--》右子树的关键字 --》跟的关键字。

###查找操作###

给定树根的指针x和关键字k，递归方式：

	--TREE-SEARCH(x,k)
	if x = NIL or k = key(x)
		then return x
	if k < key[x]
		then return TREE-SEARCH(left[x],k)
		else return TREE-SEARCH(right[x],k)

非递归方式:

	--ITERATIVE-TREE-SEARCH(x,k)
	if x = NIL or k = key(x)
		then return x
	while x != NIL and k != key[x]
		do if k < key[x]
			then x <- left[x]
			else x <- right[x]
	return x

###最大值和最小值###

（1）最大值

	--TREE-MAXIMUM(x)
	while right[x] != NIL
		do x <- right[x]
	return x

（2）最小值

	--TREE-MINIMUM(x)
	while left[x] != NIL
		do x <-left[x]
	return x

###前趋和后继###

（1）前趋

（2）后继

	TREE-SUCCESSOR(x)
	if right[x] != NIL
		then return TREE-MINIMUM(right[x])
	y <- p[x]
	while y != NIL and x = right[y]
		do x <- y
	  	  y <- p[y]
	return y

###插入和删除###

（1）插入

	--TREE-INSERT(T,z)
	y <- NIL
	x <- root[T]
	while x != NIL
		y <- x
		if key[z] < key[x]
			then x <- left[x]
			else x <- right[x]
	p[z] <- y
	if y = NIL
		then root[T] <- z
		else if key[z] < key[y]
			then left[y] <- z
			else right[y] <- z

（2）删除

删除分为三种情况：

- 若z没有子女，则修改其父结点p[z]，使NIL为其子女；
- 若z只有一个子女，则通过其子结点和父结点建立连接，来删除z；
- 若z有两个子女，则先删除z的后继y，再用y的内容来替代z的内容。

伪代码如下：

	TREE-DELETE(T,z)
	if left[z] = NIL or right[z] = NIL
		then y <- z
		else y <- TREE-SUCCESSOR(z)
	if left[y] != NIL
		then x <- left[y]
		else x <- right[y]
	if x != NIL
		then p[x] <- p[y]
	if p[y] != NIL 
		then root[T] <- x
		else if y = left[p[y]]
			then left[p[y]] <- x
			else right[p[y]] < - x
	if y != z
		then key[z] <- key[y]
	     	 copy y's satellite data into z
	return y

