---
date: 2016-3-25 19:30:30+00:00
layout: post
title: Leetcode中数组类题目小结(Easy部分)
thread: 120
categories: algorithm
tags: algorithm
---

平时空闲时刷leetcode，缺少系统性的归纳和总结。在这先小结下Leetcode中Array部分中的简单题型。目前包括的题目有：

1. Two Sum

2. Rotate Array

3. Remove Element

4. Plus one

5. Move Zeroes

6. Merge Sorted Array

7. Majority Element

8. Contains Dumplicates

9. Contains Dumplicates II

10. Pascal's Triangle

11. Pascal's Triangle II

12. Remove Duplicates from Sorted Array

13. Summary Ranges


### [Two Sum](https://leetcode.com/problems/two-sum/) ###

Given an array of integers, return indices of the two numbers such that they add up to a specific target.You may assume that each input would have exactly one solution.

Example:

Given nums = [2, 7, 11, 15], target = 9,
Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].

	{% highlight java %}
	public int[] twoSum(int[] numbers, int target)
	{
		int[] result = new int[2]();
		Map<Integer,Integer> map = new HashMap<Integer,Integer>();
		for(int i=0;i<numbers.length;i++)
		{
			if(map.containsKey(target-numbers[i]))
			{
				result[1] = i+1;
				result[0] = map.get(target - numbers[i]);
				return result;
			}
			map.put(numbers[i], i+1);
		}
		return result;
	}
	{% endhighlight %}

### [Rotate Array](https://leetcode.com/problems/rotate-array/) ###

Rotate an array of n elements to the right by k steps.

For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to [5,6,7,1,2,3,4].

Note:
Try to come up as many solutions as you can, there are at least 3 different ways to solve this problem.

	{% highlight java %}
	//Solution 1
	public void reverse(int[] nums, int start, int end)
	{
		while(start < end)
		{
			int temp = nums[start];
			nums[start] = nums[end];
			nums[end] = temp;
			start++;
			end--;
		}
	}
	public void rotateArray(int[] nums, int n, int k)
	{
		if(n==0 || k<=0)
		{
			return;
		}
		k %= n;
		reverse(nums, 0, n);
		reverse(nums, 0, k-1);
		reverse(nums, k, n);
	}
	
	//Solution 2----------------
	public void rotateArray(int[] nums, int n, int k)
	{
		if(n==0 || k<=0)
		{
			return;
		}
		int[] numsTemp = new int[n];
		for(int i=0;i<n;i++)
		{
			numsTemp[i] = nums[i];
		}
		for(int i=0;i<n;i++)
		{
			nums[(i+k)%n] = numsTemp[i];
		}
	}
	
	//Solution 3----------------
	public void rotateArray(int nums[], int n, int k)
	{
		for(;k%=n;n-=k, nums+=k)
		{
			for(int i=0;i<k;i++)
			{
				swap(nums[i], nums[n-k+1]);
			}
		}
	}
	{% endhighlight %}

### [Remove Element](https://leetcode.com/problems/remove-element/) ###


Given an array and a value, remove all instances of that value in place and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

The order of elements can be changed. It doesn't matter what you leave beyond the new length.

Example:
Given input array nums = [3,2,2,3], val = 3

Your function should return length = 2, with the first two elements of nums being 2.

	{% highlight java %}
	public int removeElement(int[] nums, int n, int value)
	{
		int m = 0;
		for(int i=0;i<n;i++)
		{
			if(nums[i] != value)
			{
				nums[m] = nums[i];
				m++; 
			}
		}
		return m;
	}
	{% endhighlight %}

### [Plus one](https://leetcode.com/problems/plus-one/) ###

Given a non-negative number represented as an array of digits, plus one to the number.

The digits are stored such that the most significant digit is at the head of the list.

	{% highlight java %}
	public int[] plusOne(int[] nums, int n)
	{
		for(int i=n-1;i>=0;i--)
		{
			if(nums[i]<9)
			{
				nums[i]++;
				return nums;
			}
			else
			{
				nums[i]=0;
			}
		}
		int[] numsTemp = new int[n+1];
		numsTemp[0] = 1;
		return numsTemp;
	}
	{% endhighlight %}

### [Move Zeroes](https://leetcode.com/problems/move-zeroes/) ###

Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.

For example, given nums = [0, 1, 0, 3, 12], after calling your function, nums should be [1, 3, 12, 0, 0].

Note:
You must do this in-place without making a copy of the array.
Minimize the total number of operations.

	{% highlight java %}
	//Solution 1
	public void moveZeroes(int[] nums, int n)
	{
		int k = 0;
		for(int i = 0;i< n;i++)
		{
			if(nums[i] != 0)
			{
				nums[k++] = nums[i];
			}
		}
		while(k<n)
		{
			nums[k++] = 0;
		}
	}
	
	//Solution 2----------------
	public void moveZeroes(int[] nums, int n)
	{
		int last = 0, cur = 0;
		while(cur<n)
		{
			if(nums[cur] != 0)
			{
				swap(nums[last], nums[cur]);
				last++;
			}
			cur++;
		}
	}
	{% endhighlight %}

### [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) ###

Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.

Note:
You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements from nums2. The number of elements initialized in nums1 and nums2 are m and n respectively.

	{% highlight java %}
	public void MergeSortedArray(int[] A, int m, int[] B, int n)
	{
		int i = m-1;
		int j = n-1;
		int k = m + n -1;
		while(i>=0 && j>=0)
		{
			if(A[i]>B[j])
			{
				A[k--] = A[i--];
			}
			else
			{
				A[k--] = B[j--];
			}
		}
		while(j>=0)
		{
			A[k--] = B[j--];
		}
	}
	{% endhighlight %}

### [Majority Element](https://leetcode.com/problems/majority-element/) ###

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

	{% highlight java %}
	//Solution 1 Moore_Voting_Algorithm
	public int majorityElement(int[] nums, int n)
	{
		int major = nums[0];
		int count = 1;
		for(int i=1;i<n;i++)
		{
			if(count == 0)
			{
				count++;
				major = nums[i];
			}
			else if(major == nums[i])
			{
				count++;
			}
			else 
			{
				count--;
			}
		}
		return major;
	}
	{% endhighlight %}

### [Contains Dumplicates](https://leetcode.com/problems/contains-duplicate/) ###

Given an array of integers, find if the array contains any duplicates. Your function should return true if any value appears at least twice in the array, and it should return false if every element is distinct.

	{% highlight java %}
	//Solution 1
	public bool ContainsDumplicates(int[] nums, int n)
	{
		for(int i=0;i<n;i++)
		{
			for(int j=i+1;j<n;j++)
			{
				if(nums[i] == nums[j])
				{
					return true;
				}
			}
		}
		return false;
	}
	
	//Solution 2----------------
	public bool ContainsDumplicates(int[] nums, int n)
	{
		quickSort(nums);
		for(int i=1;i<n;i++)
		{
			if(nums[i] == nums[i-1])
			{
				return true;
			}
		}
		return false;
	}
	{% endhighlight %}

### [Contains Dumplicates II](https://leetcode.com/problems/contains-duplicate-ii/) ###

Given an array of integers and an integer k, find out whether there are two distinct indices i and j in the array such that nums[i] = nums[j] and the difference between i and j is at most k.

	{% highlight java %}
	public void containsNearbyDumplicates(int[] nums, int n)
	{
		Map<int,int> map = new HashMap<int,int>();
		for(int i=0;i<n;i++)
		{
			if(map.containsKey(nums[i])&&(i-map.get(nums[i])<=k))
			{
				return true;
			}
			map.put(nums[i],i);
		}
		return false;
	}
	{% endhighlight %}

### [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) ###

Given numRows, generate the first numRows of Pascal's triangle.

For example, given numRows = 5,
Return

[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]


### [Pascal's Triangle II](https://leetcode.com/problems/pascals-triangle-ii/) ###

Given an index k, return the kth row of the Pascal's triangle.

For example, given k = 3,
Return [1,3,3,1].

Note:
Could you optimize your algorithm to use only O(k) extra space?


### [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) ###

Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.

Do not allocate extra space for another array, you must do this in place with constant memory.

For example,
Given input array nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively. It doesn't matter what you leave beyond the new length.

	{% highlight java %}
	public int removeDuplicates(int nums[], int n)
	{
		if(n<2)
		{
			return;
		}
		int k = 1;
		for(int i = 1;i<n;i++)
		{
			if(nums[i] != nums[i-1])
			{
				nums[k++] = nums[i];
			}
		}
		return k;
	}
	{% endhighlight %}

### [Summary Ranges](https://leetcode.com/problems/summary-ranges/) ###

Given a sorted integer array without duplicates, return the summary of its ranges.

For example, given [0,1,2,4,5,7], return ["0->2","4->5","7"].

	{% highlight java %}
	//Summary Ranges
	public vector<String> summaryRanges(int[] nums, int n)
	{
		List<String> list = new ArrayList<String>();
		if(n==1)
		{
			list.add(nums[0] + "");
			return list;
		}
		for(int i = 0;i<n;i++)
		{
			int a= nums[i];
			while(i+1<n&&(nums[i+1]-nums[i]==1))
			{
				i++;
			}
			if(a!=nums[i])
			{
				list.add(a+"->"+nums[i]);
			}
			else
			{
				list.add(a+"");
			}
		}
		return list;
	}
	{% endhighlight %}




