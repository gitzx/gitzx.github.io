---
date: 2013-12-12 22:50:30+00:00
layout: post
title: 利用ichartjs库来实现Android上绘制报表
thread: 12
categories: algorithm
tags:  algorithm
---

打算抽时间看《算法导论》，重新学习算法知识。第一篇就小结下六个常见的比较排序算法。

###冒泡排序###
冒泡排序：相邻两元素两两比较，一步一步往上升。时间复杂度为O（n2），伪代码如下：

	for i<- 1 to length(A)
		for j<-length(A) downto i+1
	   		do if A[j]<A[j-1}
	       			 then exchange A[j] <-> A[j-1]

