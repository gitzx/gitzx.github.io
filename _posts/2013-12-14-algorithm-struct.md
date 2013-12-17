---
date: 2013-12-14 22:25:30+00:00
layout: post
title: 链表、队列、栈和堆
thread: 14
categories: algorithm
tags:  algorithm
---

在这小结下数据结构链表、队列、栈和堆的性质和一些基本操作。

###链表###

链表中各对象按线性顺序排序，顺序有各对象的指针决定。按是否排序可分为已排序和未排序；按结构可分为单链表（没有前驱的prev指针）、双向链表和环形链表。下面的操作的链表都是未排序且时双向链表。

（1）链表的搜索操作

	--LIST-SEARCH(L,k)
	x <- head[L]
	while x!=NIL and key[x] != k
		x <- next[x]
	return x

（2）链表的插入操作（将x插入到链表的前端）

	--LIST-INSERT(L,x)
	next[x] <- head[L]
	if head[L] != NIL
		prev[head[L]] <- x
	head[L] <- x
	prev[x] <- NIL

（3）链表的删除操作

	--LIST-DELETE(L,x)
	if prev[x] != NIL
		then next[prev[x]] <- next[x]
		else head[x] <- next[x]
	if next[x] != NIL
		prev[next[x]] <- prev[x]

###队列###

队列的特点是先进先出。

（1）入队

	--ENQUEUE(Q,x)
	Q[tail[Q]] <- x
	if tail[Q] = length[Q]
		then tail[Q] <- 1
		else tail[Q] <- tail[Q]+1


（2）出队

	--DEQUEUE(Q)
	x <- Q[head[Q]]
	if head[Q] = length[Q]
		then head[Q] <- 1
		else head[Q] <- head[Q] + 1
	return x

###栈###

栈的特点是后进先出。

（1）判断栈是否为空

	--STACK-EMPTY(S)
	if top[S] = 0
		then return TRUE
		else return FALSE

（2）入栈

	--PUSH(S,x)
	top[S] <- top [S] + 1
	S[top[S]] <- x

（3）出栈

	--POP(S)
	if STACK-EMPTY(S)
		then error "underflow"
		else top[S] <- top[S] - 1
			return S[top[S]+1]

