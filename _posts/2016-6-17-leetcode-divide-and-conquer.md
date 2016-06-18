---
date: 2016-6-17 12:21:30+00:00
layout: post
title: Leetcode中分治算法类题目小结
thread: 141
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中分治算法类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Search a 2D Matrix II

2. Different Ways to Add Parentheses

3. Count of Smaller Numbers After Self

4. Count of Range Sum

5. Burst Balloons

6. Expression Add Operators


### [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) ###

Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

1. Integers in each row are sorted in ascending from left to right.

2. Integers in each column are sorted in ascending from top to bottom.

For example,

Consider the following matrix:

	[
	  [1,   4,  7, 11, 15],
	  [2,   5,  8, 12, 19],
	  [3,   6,  9, 16, 22],
	  [10, 13, 14, 17, 24],
	  [18, 21, 23, 26, 30]
	]

Given target = 5, return true.

Given target = 20, return false.

	{% highlight java %}
	public boolean searchMatrix(int[][] matrix,int target)
	{
		int m=matrix.length-1;
		int n=matrix[0].length-1;
		int i=m;
		int j=0;
		while(i>=0&&j<=n)
		{
			if(target<matrix[i][j])
			{
				i--;
			}
			else if(target>matrix[i][j])
			{
				j++;
			}
			else
			{
				return true;
			}
		}
		return false;
	}
	{% endhighlight %}

### [Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/) ###

Given a string of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators. The valid operators are +, - and *.

Example 1

Input: "2-1-1".

	((2-1)-1) = 0
	(2-(1-1)) = 2
	Output: [0, 2]

Example 2

Input: "2*3-4*5"

	(2*(3-(4*5))) = -34
	((2*3)-(4*5)) = -14
	((2*(3-4))*5) = -10
	(2*((3-4)*5)) = -10
	(((2*3)-4)*5) = 10

Output: [-34, -14, -10, -10, 10]

	{% highlight java %}
	//solution1 
	public class Solution
	{
		public List<Integer> diffWaysToCompute(String input)
		{
			List<Integer> ret=new LinkedList<Integer>();
			for(int i=0;i<input.length();i++)
			{
				if(input.charAt(i)=='+'||
					input.charAt(i)=='-'||
					input.charAt(i)=='*')
				{
					String part1=input.substring(0,i);
					String part2=input.substring(i+1);
					List<Integer> part1Ret=diffWaysToCompute(part1);
					List<Integer> part2Ret=diffWaysToCompute(part2);
					for(Integer p1:part1Ret)
					{
						for(Integer p2:part2Ret)
						{
							int c=0;
							switch(input.charAt(i))
							{
								case '+':
								{
									c=p1+p2;
									break;
								}
								case '-':
								{
									c=p1-p2;
									break;
								}
								case '*':
								{
									c=p1*p2;
									break;
								}
							}
							ret.add(c);
						}
					}
				}
			}
			if(ret.size()==0)
			{
				ret.add(Integer.valueOf(input));
			}
			return ret;
		}
	}
	{% endhighlight %}

### [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) ###

You are given an integer array nums and you have to return a new counts array. The counts array has the property where counts[i] is the number of smaller elements to the right of nums[i].

Example:

	Given nums = [5, 2, 6, 1]
	
	To the right of 5 there are 2 smaller elements (2 and 1).
	To the right of 2 there is only 1 smaller element (1).
	To the right of 6 there is 1 smaller element (1).
	To the right of 1 there is 0 smaller element.

Return the array [2, 1, 1, 0].

	{% highlight java %}
	//solution1
	public List<Integer> countSmaller(int[] nums)
	{
		Integer[] ans=new Integer[nums.length];
		List<Integer> sorted=new ArrayList<Integer>();
		for(int i=nums.length-1;i>=0;i--)
		{
			int index=findIndex(sorted,nums[i]);
			ans[i]=index;
			sorted.add(index,nums[i]);
		}
		return Arrays.asList(ans);
	}
	private int findIndex(List<Integer> sorted,int target)
	{
		if(sorted.size()==0)
		{
			return 0;
		}
		int start=0;
		int end=sorted.size()-1;
		if(sorted.get(end)<target)
		{
			return end+1;
		}
		if(sorted.get(start)>=target)
		{
			return 0;
		}
		while(start+1<end)
		{
			int mid=start+(end-start)/2;
			if(sorted.get(mid)<target)
			{
				start=mid+1;
			}
			else
			{
				end=mid;
			}
		}
		if(sorted.get(start)>=target)
		{
			return start;
		}
		return end;
	}
	{% endhighlight %}

### [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) ###

Given an integer array nums, return the number of range sums that lie in [lower, upper] inclusive.

Range sum S(i, j) is defined as the sum of the elements in nums between indices i and j (i ≤ j), inclusive.

Note:

A naive algorithm of O(n2) is trivial. You MUST do better than that.

Example:

Given nums = [-2, 5, -1], lower = -2, upper = 2,

Return 3.

The three ranges are : [0, 0], [2, 2], [0, 2] and their respective sums are: -2, -1, 2.



### [Burst Balloons](https://leetcode.com/problems/burst-balloons/) ###

Given n balloons, indexed from 0 to n-1. Each balloon is painted with a number on it represented by array nums. You are asked to burst all the balloons. If the you burst balloon i you will get nums[left] * nums[i] * nums[right] coins. Here left and right are adjacent indices of i. After the burst, the left and right then becomes adjacent.

Find the maximum coins you can collect by bursting the balloons wisely.

Note: 

(1) You may imagine nums[-1] = nums[n] = 1. They are not real therefore you can not burst them.

(2) 0 ≤ n ≤ 500, 0 ≤ nums[i] ≤ 100

Example:

Given [3, 1, 5, 8]

Return 167

    nums = [3,1,5,8] --> [3,5,8] -->   [3,8]   -->  [8]  --> []
    coins =  3*1*5      +  3*5*8    +  1*3*8      + 1*8*1   = 167

代码实现如下：

### [Expression Add Operators](https://leetcode.com/problems/expression-add-operators/) ###

Given a string that contains only digits 0-9 and a target value, return all possibilities to add binary operators (not unary) +, -, or * between the digits so they evaluate to the target value.

Examples: 

	"123", 6 -> ["1+2+3", "1*2*3"] 
	"232", 8 -> ["2*3+2", "2+3*2"]
	"105", 5 -> ["1*0+5","10-5"]
	"00", 0 -> ["0+0", "0-0", "0*0"]
	"3456237490", 9191 -> []

代码实现如下：