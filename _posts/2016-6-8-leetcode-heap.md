---
date: 2016-6-8 10:06:30+00:00
layout: post
title: Leetcode中Heap类题目小结
thread: 137
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Heap类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Kth Largest Element in an Array

2. Find Median from Data Stream

3. Sliding Window Maximum

4. The Skyline Problem


### [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) ###


Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order, not the kth distinct element.

For example,
Given [3,2,1,5,6,4] and k = 2, return 5.

Note: 
You may assume k is always valid, 1 ≤ k ≤ array's length.

	{% highlight java %}
	//solution1 sort
	public int findKthLargest(int[] nums,int k)
	{
		Arrays.sort(nums);
		return nums[nums.length-k];
	}
	//solution2 Heap
	public int findKthLargest(int[] nums,int k)
	{
		PriorityQueue<Integer> q=new PriorityQueue<Integer>(k);
		for(int i:nums)
		{
			q.offer(i);
			if(q.size()>k)
			{
				q.poll();
			}
		}
		return q.peek();
	}
	{% endhighlight %}

### [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) ###

Median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle value.

Examples: 

[2,3,4] , the median is 3

[2,3], the median is (2 + 3) / 2 = 2.5

Design a data structure that supports the following two operations:

1. void addNum(int num) - Add a integer number from the data stream to the data structure.

2. double findMedian() - Return the median of all elements so far.

For example:

	add(1)
	add(2)
	findMedian() -> 1.5
	add(3) 
	findMedian() -> 2

实现如下：

	{% highlight java %}
	class medianFinder
	{
		PriorityQueue<Integer> maxHeap; //lower half
		PriorityQueue<Integer> minHeap; //higher half
		public medianFinder()
		{
			maxHeap=new PriorityQueue<Integer>(Collections.reverseOrder());
			minHeap=new PriorityQueue<Integer>();
		}
		public void addNum(int num)
		{
			maxHeap.offer(num);
			minHeap.offer(maxHeap.poll());
			if(maxHeap.size()<minHeap.size())
			{
				maxHeap.offer(minHeap.poll());
			}
		}
		public double findMedian()
		{
			if(maxHeap.size()==minHeap.size())
			{
				return (double)(maxHeap.peek()+minHeap.peek())/2;
			}
			else
			{
				return maxHeap.peek();
			}
		}
	}
	{% endhighlight %}

### [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) ###

Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.

For example,

Given nums = [1,3,-1,-3,5,3,6,7], and k = 3.

	Window position                Max
	---------------               -----
	[1  3  -1] -3  5  3  6  7       3
	 1 [3  -1  -3] 5  3  6  7       3
	 1  3 [-1  -3  5] 3  6  7       5
	 1  3  -1 [-3  5  3] 6  7       5
	 1  3  -1  -3 [5  3  6] 7       6
	 1  3  -1  -3  5 [3  6  7]      7

Therefore, return the max sliding window as [3,3,5,5,6,7].

Note: 

You may assume k is always valid, ie: 1 ≤ k ≤ input array's size for non-empty array.

	{% highlight java %}
	public int[] maxSlidingWindow(int[] nums,int k)
	{
		if(nums==null||nums.length==0)
		{
			return new int[0];
		}
		int[] result=new int[nums.length-k+1];
		LinkedList<Integer> deque=new LinkedList<Integer>();
		for(int i=0;i<nums.length;i++)
		{
			if(!deque.isEmpty()&&deque.peekFirst()==i-k)
			{
				deque.poll();
			}
			while(!deque.isEmpty()&&nums[deque.peekLast()]<nums[i])
			{
				deque.removeLast();
			}
			deque.offer(i);
			if(i+1>=k)
			{
				result[i+1-k]=nums[deque.peek()];
			}
		}
		return result;
	}
	{% endhighlight %}

### [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) ###

A city's skyline is the outer contour of the silhouette formed by all the buildings in that city when viewed from a distance. Now suppose you are given the locations and height of all the buildings as shown on a cityscape photo (Figure A), write a program to output the skyline formed by these buildings collectively (Figure B).

 Buildings  Skyline Contour

The geometric information of each building is represented by a triplet of integers [Li, Ri, Hi], where Li and Ri are the x coordinates of the left and right edge of the ith building, respectively, and Hi is its height. It is guaranteed that 0 ≤ Li, Ri ≤ INT_MAX, 0 < Hi ≤ INT_MAX, and Ri - Li > 0. You may assume all buildings are perfect rectangles grounded on an absolutely flat surface at height 0.

For instance, the dimensions of all buildings in Figure A are recorded as: [ [2 9 10], [3 7 15], [5 12 12], [15 20 10], [19 24 8] ] .

The output is a list of "key points" (red dots in Figure B) in the format of [ [x1,y1], [x2, y2], [x3, y3], ... ] that uniquely defines a skyline. A key point is the left endpoint of a horizontal line segment. Note that the last key point, where the rightmost building ends, is merely used to mark the termination of the skyline, and always has zero height. Also, the ground in between any two adjacent buildings should be considered part of the skyline contour.

For instance, the skyline in Figure B should be represented as:[ [2 10], [3 15], [7 12], [12 0], [15 10], [20 8], [24, 0] ].

Notes:

1. The number of buildings in any input list is guaranteed to be in the range [0, 10000].

2. The input list is already sorted in ascending order by the left x position Li.

3. The output list must be sorted by the x position.

4. There must be no consecutive horizontal lines of equal height in the output skyline. For instance, [...[2 3], [4 5], [7 5], [11 5], [12 7]...] is not acceptable; the three lines of height 5 should be merged into one in the final output as such: [...[2 3], [4 5], [12 7], ...]