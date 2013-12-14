---
date: 2013-12-12 22:50:30+00:00
layout: post
title: 六个常见的比较排序算法
thread: 12
categories: algorithm
tags:  algorithm
---

打算抽时间重新学习下算法知识。第一篇就小结下六个常见的比较排序算法。

###冒泡排序###
冒泡排序：相邻两元素两两比较，一步步往上升。时间复杂度O（n2），伪代码如下：

	for i<- 1 to length(A)
		for j<-length(A) downto i+1
	   		do if A[j]<A[j-1}
	       			 then exchange A[j] <-> A[j-1]

###直接插入排序###
插入排序：类似扑克牌插入，将后面的元素插入到前面合适的位置。时间复杂度O（n2）,伪代码如下：

	for i<- 2 to length(A)
   		do key<- A[i]
     		     j<-i-1
      		     while j>0 and A[j]>key
			           A[j+1] <- A[j]
	    		       j <- j-1
      		    A[i+1] <- key

###直接选择排序###
选择排序：首先找出A中最小的元素，与A[1]交换，再找出第二小的元素，与A[2]交换，依次下去。时间复杂度O（n2），伪代码如下：

	for i<-1 to length(A)-1
		do min <- i
	  	     for j <- i-1 to length(A)
			  then if A[j] < A[min]
				  then min <- j
	   	    exchange A[i] <-> A[min]

###希尔排序###

希尔排序：又称缩小增量插入排序。先取一个小于n的整数d1作为第一个增量，把文件的全部记录分成d1个组。所有距离为d1的倍数的记录放在同一个组中。先在各组内进行直接插入排序；然后，取第二个增量d2<d1重复上述的分组和排序，直至所取的增量dt=1(dt<dt-l<…<d2<d1)，即所有记录放在同一组中进行直接插入排序为止。时间复杂度未知，伪代码如下（取d1=n/2）：

	d <- round(n/2)
	while n > 0
		for i <- d-1 to n 
			key <- A[i]
			j <- i-d
			while j > 0 and A[j] >key
				A[j+d] <- A[j]
				j <- j-d
			A[j+d] <- A[j]
		d <- round(d/2)

###快速排序###
快速排序：设A中最后一个元素为基准，划分两个子数组，使得左边的子数组小于基准，右边的子数组大于基准，再在子数组中继续排序，其中要计算分界下标。平均时间复杂度为O（nlogn）,最坏情况为O(n2)。伪代码如下（递归方式实现，非递归的以后再实现）如下：

	--QuickSort(A,p,r)
	if p < r
		q <- partition(A,p,r)
		QuickSort(A,p,q-1)
		QuickSort(A,q+1,r)

计算分界下标的伪代码如下：

	--partition(A,p,r)
	key <- A[r]
	i <- p-1
	for j <- p to r-1
		if A[j] <= key
			i <- i+1
			exchange A[j] <-> A[i]
	exchange A[i+1] <-> A[r]
	return i+1

###堆排序###
堆排序：分为三个部分（1.保持堆；2.建堆；3.排序）。时间复杂度为O（nlogn）。堆分为最大堆和最小堆。以最大堆排序，伪代码如下：

（1）保持堆的性质（其中heap-size(A)为存放在数组A中的元素个数）

	--MAX-HEAPIFY(A,i)
	l <- LEFT(i)
	r <- RIGHT(i)
	if l <= heap-size(A) and A[l] > A[i]
		then largest <- l
		else largest <- i
	if r <= heap-size(A) and A[r] > A[largest]
		then largest <-r
	if largest != i
		then exchange A[i] <-> A[largest}
		   MAX_HEAPIFY(A,largest)

（2）建堆

	--BUILD-MAX-HEAP(A)
	heap-size(A) <- length(A)
	for i <- length[A]/2 downto 1
		MAX-HEAPIFY(A,i)

（3）排序

	--HEAPSORT(A)
	BUILD-MAX-HEAP(A)
	for i <- length[A] downto 2
		exchange A[1] <-> A[i]
		heap-size[A] <- heap-size[A]-1
		MAX-HEAPIFY(A,i)


排序的python实现可见[排序的python实现](https://github.com/gitzx/Algorithm_exercise/blob/master/sort/sort_python.py)




