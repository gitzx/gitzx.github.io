---
date: 2016-6-14 18:48:30+00:00
layout: post
title: Leetcode中两种图遍历算法类题目小结
thread: 139
categories: algorithm
tags: algorithm

---

深度优先遍历和广度优先遍历是图遍历的两种常用算法，这篇小结下Leetcode中深度优先遍历和广度优先遍历类部分的题目，目前已有的题目(除去之前已总结的)有：

1. Remove Invalid Parentheses

2. Longest Increasing Path in a Matrix

3. Number of Islands

4. Surrounded Regions


### [Remove Invalid Parentheses](https://leetcode.com/problems/remove-invalid-parentheses/) ###

Remove the minimum number of invalid parentheses in order to make the input string valid. Return all possible results.

Note: The input string may contain letters other than the parentheses ( and ).

Examples:

	"()())()" -> ["()()()", "(())()"]
	"(a)())()" -> ["(a)()()", "(a())()"]
	")(" -> [""]

代码实现如下:

	{% highlight java %}
	public class Solution
	{
		ArrayList<String> result=new ArrayList<String>();
		int max=0;
		public List<String> removeInvalidParentheses(String s)
		{
			if(s==null)
			{
				return result;
			}
			dfs(s,"",0,0);
			if(result.size()==0)
			{
				result.add("");
			}
			return result;
		}
		public void dfs(String left,String right,int countLeft,int maxLeft)
		{
			if(left.length()==0)
			{
				if(countLeft==0&&right.length()!=0)
				{
					if(maxLeft>max)
					{
						max=maxLeft;
					}
					if(maxLeft==max&&!result.contains(right))
					{
						result.add(right);
					}
				}
				return;
			}
			if(left.charAt(0)=='(')
			{
				dfs(left.substring(1),right+"(",countLeft+1,maxLeft+1);
				dfs(left.substring(1),right,countLeft,maxLeft);
			}
			else if(left.charAt(0)==')')
			{
				if(countLeft>0)
				{
					dfs(left.substring(1),right+")",countLeft-1,maxLeft);
				}
				dfs(left.substring(1),right,countLeft,maxLeft);
			}
			else
			{
				dfs(left.substring(1),right+String.valueOf(left.charAt(0)),countLeft,maxLeft);
			}
		}
	}
	{% endhighlight %}

### [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) ### 

Given an integer matrix, find the length of the longest increasing path.

From each cell, you can either move to four directions: left, right, up or down. You may NOT move diagonally or move outside of the boundary (i.e. wrap-around is not allowed).

Example 1:

	nums = [
	  [9,9,4],
	  [6,6,8],
	  [2,1,1]
	]

Return 4

The longest increasing path is [1, 2, 6, 9].

Example 2:

	nums = [
	  [3,4,5],
	  [3,2,6],
	  [2,2,1]
	]

Return 4

The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.


### [Number of Islands](https://leetcode.com/problems/number-of-islands/) ###

Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:

	11110
	11010
	11000
	00000

Answer: 1

Example 2:

	11000
	11000
	00100
	00011

Answer: 3


### [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) ###

Given a 2D board containing 'X' and 'O', capture all regions surrounded by 'X'.

A region is captured by flipping all 'O's into 'X's in that surrounded region.

For example,

	X X X X
	X O O X
	X X O X
	X O X X

After running your function, the board should be:

	X X X X
	X X X X
	X X X X
	X O X X

Subscribe to see which companies asked this question