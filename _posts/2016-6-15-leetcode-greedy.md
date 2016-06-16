---
date: 2016-6-15 17:03:30+00:00
layout: post
title: Leetcode中贪婪算法类题目小结
thread: 140
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中贪婪算法类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Gas Station

2. Patching Array

3. Create Maximum Number

4. Candy


### [Gas Station](https://leetcode.com/problems/gas-station/) ###

There are N gas stations along a circular route, where the amount of gas at station i is gas[i].

You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from station i to its next station (i+1). You begin the journey with an empty tank at one of the gas stations.

Return the starting gas station's index if you can travel around the circuit once, otherwise return -1.

Note:
The solution is guaranteed to be unique.

	{% highlight java %}
	public int canCompleteCircuit(int[] gas,int[] cost)
	{
		int sumRemain=0;
		int total=0;
		int start=0;
		for(int i=0;i<gas.length;i++)
		{
			int remain=gas[i]-cost[i];
			if(sumRemain>=0)
			{
				sumRemain+=remain;
			}
			else
			{
				sumRemain=remain;
				start=i;
			}
		}
		if(total>=0)
		{
			return start;
		}
		else
		{
			return -1;
		}
	}
	{% endhighlight %}

### [Patching Array](https://leetcode.com/problems/patching-array/) ###

Given a sorted positive integer array nums and an integer n, add/patch elements to the array such that any number in range [1, n] inclusive can be formed by the sum of some elements in the array. Return the minimum number of patches required.

Example 1:

nums = [1, 3], n = 6

Return 1.

Combinations of nums are [1], [3], [1,3], which form possible sums of: 1, 3, 4.
Now if we add/patch 2 to nums, the combinations are: [1], [2], [3], [1,3], [2,3], [1,2,3].

Possible sums are 1, 2, 3, 4, 5, 6, which now covers the range [1, 6].

So we only need 1 patch.

Example 2:

nums = [1, 5, 10], n = 20

Return 2.

The two patches can be [2, 4].

Example 3:

nums = [1, 2, 2], n = 5

Return 0.

	{% highlight java %}
	//if nums[i]<=miss [0,miss+nums[i]]
	//if nums[i]>miss  [0,miss+miss]
	public int minPatches(int[] nums,int n)
	{
		long miss=1;
		int count=0;
		int i=0;
		while(miss<=n)
		{
			if(i<nums.length&&nums[i]<=miss)
			{
				miss=miss+nums[i];
				i++;
			}
			else
			{
				miss+=miss;
				count++;
			}
		}
		return result;
	}
	{% endhighlight %}

### [Create Maximum Number](https://leetcode.com/problems/create-maximum-number/) ###

Given two arrays of length m and n with digits 0-9 representing two numbers. Create the maximum number of length k <= m + n from digits of the two. The relative order of the digits from the same array must be preserved. Return an array of the k digits. You should try to optimize your time and space complexity.

Example 1:

nums1 = [3, 4, 6, 5]

nums2 = [9, 1, 2, 5, 8, 3]

k = 5

return [9, 8, 6, 5, 3]

Example 2:

nums1 = [6, 7]

nums2 = [6, 0, 4]

k = 5

return [6, 7, 6, 0, 4]


Example 3:

nums1 = [3, 9]

nums2 = [8, 9]

k = 3

return [9, 8, 9]

### [Candy](https://leetcode.com/problems/candy/) ###

There are N children standing in a line. Each child is assigned a rating value.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.

Children with a higher rating get more candies than their neighbors.

What is the minimum candies you must give?

	{% highlight java %}
	public int candy(int[] ratings)
	{
		int candies[]=new int[ratings.length];
		Arrays.fill(candies,1);
		for(int i=1;i<candies.length;i++)
		{
			if(ratings[i]>ratings[i-1])
			{
				candies[i]=candies[i-1]+1;
			}
		}
		for(int i=candies.length-2;i>=0;i--)
		{
			if(ratings[i]>ratings[i+1])
			{
				candies[i]=Math.max(candies[i],candies[i+1]+1);
			}
		}
		int sum=0;
		for(int candy:candies)
		{
			sum+=candy;
		}
		return sum;
	}
	{% endhighlight %}