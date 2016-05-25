---
date: 2016-5-20 18:21:30+00:00
layout: post
title: Leetcode中数字类题目小结（Hard部分）
thread: 134
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Math类Hard部分的题目，目前已有的题目(除去之前已总结的)有：

1. Number of Digit One

2. Basic Calculator

3. Self Crossing

4. Max Points on a Line


### [Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) ###

Given an integer n, count the total number of digit 1 appearing in all non-negative integers less than or equal to n.

For example:

Given n = 13,

Return 6, because digit 1 occurred in the following numbers: 1, 10, 11, 12, 13.

	{% highlight java %}
	public int countDigitOne(int n)
	{
		int ones=0;
		for(long long m=1;m<=n;m*=10)
		{
			int a=n/m, b=n%m;
			ones+=(a+8)/10*m+(a%10==1)*(b+1);
		}
		return ones;
	}
	{% endhighlight %}

### [Basic Calculator](https://leetcode.com/problems/basic-calculator/) ###

Implement a basic calculator to evaluate a simple expression string.

The expression string may contain open ( and closing parentheses ), the plus + or minus sign -, non-negative integers and empty spaces .

You may assume that the given expression is always valid.

	Some examples:
	"1 + 1" = 2
	" 2-1 + 2 " = 3
	"(1+(4+5+2)-3)+(6+8)" = 23

Note: Do not use the eval built-in library function.

	{% highlight java %}
	public int calculate(String s)
	{
		Stack<Integer> stack=new Stack<Integer>();
		int result=0;
		int number=0;
		int sign=1;
		for(int i=0;i<s.length();i++)
		{
			char c=s.charAt(i);
			if(Character.isDigit(c))
			{
				number=10*number+(int)(c-'0');
			}
			else if(c=='+')
			{
				result+=sign*number;
				number=0;
				sign=1;
			}
			else if(c=='-')
			{
				result-=sign*number;
				number=0;
				sign=-1;
			}
			else if(c=='(')
			{
				stack.push(result);
				stack.push(sign);
				sign=1;
				result=0;
			}
			else if(c==')')
			{
				result+=sign*number;
				number=0;
				result*=stack.pop();
				result+=stack.pop();
			}
		}
		if(number!=0)
		{
			result+=sign*number;
		}
		return result;
	}
	{% endhighlight %}

### [Self Crossing](https://leetcode.com/problems/self-crossing/) ###

You are given an array x of n positive numbers. You start at point (0,0) and moves x[0] metres to the north, then x[1] metres to the west, x[2] metres to the south, x[3] metres to the east and so on. In other words, after each move your direction changes counter-clockwise.

Write a one-pass algorithm with O(1) extra space to determine, if your path crosses itself, or not.

Example 1:

	Given x = [2, 1, 1, 2],
	┌───┐
	│   │
	└───┼──>
	    │

	Return true (self crossing)

Example 2:

	Given x = [1, 2, 3, 4],
	┌──────┐
	│      │
	│
	│
	└────────────>

	Return false (not self crossing)

Example 3:

	Given x = [1, 1, 1, 1],
	┌───┐
	│   │
	└───┼>
	
	Return true (self crossing)



### [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) ###

Given n points on a 2D plane, find the maximum number of points that lie on the same straight line.