---
date: 2016-5-16 19:03:30+00:00
layout: post
title: Leetcode中数字类题目小结（Medium部分）
thread: 133
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Math类Medium部分的题目，目前已有的题目(除去之前已总结的)有：

1. Perfect Squares 	

2. Sqrt(x)

3. Fraction to Recurring Decimal

4. Integer Break

5. Ugly Number II

6. Divide Two Integers

7. Bulb Switcher

8. Pow(x, n)

9. Super Ugly Number

10. Permutation Sequence


### [Perfect Squares](https://leetcode.com/problems/perfect-squares/) ###

Given a positive integer n, find the least number of perfect square numbers (for example, 1, 4, 9, 16, ...) which sum to n.

For example, given n = 12, return 3 because 12 = 4 + 4 + 4; given n = 13, return 2 because 13 = 4 + 9.

	{% highlight java %}
	//solution 1 dp
	public int numSquares(int n)
	{
		int max=(int)Math.sqrt(n);
		int[] dp=new int[n+1];
		Arrays.fill(dp,Integer.MAX_VALUE);
		for(int i=1;i<=n;i++)
		{
			for(int j=1;j<=max;j++)
			{
				if(i==j*j)
				{
					dp[i]=1;
				}
				else
				{
					dp[i]=Math.min(dp[i],dp[i-j*j]+1);
				}
			}
		}
		return dp[n];
	}
	{% endhighlight %}

### [Sqrt(x)](https://leetcode.com/problems/sqrtx/) ###


Implement int sqrt(int x).

Compute and return the square root of x.

	{% highlight java %}
	//solution 1 Newton method
	public int sqrt(int x)
	{
		long r=x;
		while(r*r>x)
		{
			r=(r+x/r)/2;
		}
		return (int)r;
	}
	//solution 2 binary search
	public int sqrt(int x)
	{
		if(x==0)
		{
			return 0;
		}
		int left=1,right=Integer.MAX_VALUE;
		while(true)
		{
			int mid=(right+left)/2;
			if(mid>x/mid)
			{
				right=mid-1;
			}
			else
			{
				if(mid+1>x/(mid+1))
				{
					return mid;
				}
				left=mid+1;
			}
		}
	}
	{% endhighlight %}

### [Fraction to Recurring Decimal](https://leetcode.com/problems/fraction-to-recurring-decimal/) ###

Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.

If the fractional part is repeating, enclose the repeating part in parentheses.

For example,

Given numerator = 1, denominator = 2, return "0.5".

Given numerator = 2, denominator = 1, return "2".

Given numerator = 2, denominator = 3, return "0.(6)".


### [Integer Break](https://leetcode.com/problems/integer-break/) ###

Given a positive integer n, break it into the sum of at least two positive integers and maximize the product of those integers. Return the maximum product you can get.

For example, given n = 2, return 1 (2 = 1 + 1); given n = 10, return 36 (10 = 3 + 3 + 4).

Note: you may assume that n is not less than 2.

	{% highlight java %}
	public int integerBreak(int n)
	{
		if(n==2)
		{
			return 1;
		}
		else if(n==3)
		{
			return 2;
		}
		else if(n%3==0)
		{
			return (int)Math.pow(3,n/3);
		}
		else if(n%3==1)
		{
			return 2*2*(int)Math.pow(3,(n-4)/3);
		}
		else
		{
			return 2*(int)Math.pow(3,n/3);
		}
	}
	{% endhighlight %}

### [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) ###


Write a program to find the n-th ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5. For example, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 is the sequence of the first 10 ugly numbers.

Note that 1 is typically treated as an ugly number.


### [Divide Two Integers](https://leetcode.com/problems/divide-two-integers/) ###

Divide two integers without using multiplication, division and mod operator.

If it is overflow, return MAX_INT.

	{% highlight java %}
	public int divide(int dividend,int divisor)
	{
		if(!divisor||(dividend==INT_MIN&&divisor==-1))
		{
			return INT_MAX;
		}
		int sign=((dividend<0)^(divisor<0))?-1:1;
		long long dvd=labs(dividend);
		long long dvs=labs(divisor);
		int res=0;
		while(dvd>=dvs)
		{
			long long temp=dvs, multiple=1;
			while(dvd>=(temp<<1))
			{
				temp<<=1;
				multiple<<=1;
			}
			dvd-=temp;
			res+=multiple;
		}
		return sign==1?res:-res;
	}
	{% endhighlight %}

### [Bulb Switcher](https://leetcode.com/problems/bulb-switcher/) ###

There are n bulbs that are initially off. You first turn on all the bulbs. Then, you turn off every second bulb. On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the ith round, you toggle every i bulb. For the nth round, you only toggle the last bulb. Find how many bulbs are on after n rounds.

Example:

Given n = 3. 

	At first, the three bulbs are [off, off, off].

	After first round, the three bulbs are [on, on, on].

	After second round, the three bulbs are [on, off, on].

	After third round, the three bulbs are [on, off, off]. 
	
	So you should return 1, because there is only one bulb is on.

实现如下：

	{% highlight java %}
	//solution 1
	public int bulbSwitch(int n)
	{
		return sqrt(n);
	}
	//solution 2
	public int bulbSwitch(int n)
	{
		int count=0;
		for(int i=1;i*i<=n;i++)
		{
			++count;
		}
		return count;
	}
	{% endhighlight %}

### [Pow(x, n)](https://leetcode.com/problems/powx-n/) ###

Implement pow(x, n).

	//solution 1 iterative
	public double myPow(double x,int n)
	{
		if(n==0)
		{
			return 1;
		}
		if(n<0)
		{
			n=-n;
			x=1/x;
		}
		double ans=1;
		while(n>0)
		{
			if(n&1)
			{
				ans*=x;
			}
			x*=x;
			n>>=1;
		}
		return ans;
	}
	//solution 2
	public double myPow(double x,int n)
	{
		if(n==0)
		{
			return 1;
		}
		if(n<0)
		{
			n=-n;
			x=1/x;
		}
		return (n%2==0)?myPow(x*x,n/2):x*myPow(x*x,n/2);
	}

### [Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) ###

Write a program to find the nth super ugly number.

Super ugly numbers are positive numbers whose all prime factors are in the given prime list primes of size k. For example, [1, 2, 4, 7, 8, 13, 14, 16, 19, 26, 28, 32] is the sequence of the first 12 super ugly numbers given primes = [2, 7, 13, 19] of size 4.

Note:

(1) 1 is a super ugly number for any given primes.

(2) The given numbers in primes are in ascending order.

(3) 0 < k ≤ 100, 0 < n ≤ 106, 0 < primes[i] < 1000.


### [Permutation Sequence](https://leetcode.com/problems/permutation-sequence/) ###

The set [1,2,3,…,n] contains a total of n! unique permutations.

By listing and labeling all of the permutations in order,
We get the following sequence (ie, for n = 3):

"123"
"132"
"213"
"231"
"312"
"321"
Given n and k, return the kth permutation sequence.

Note: Given n will be between 1 and 9 inclusive.

	{% highlight java %}
	public String getPermutation(int n,int k)
	{
		int pos=0;
		List<Integer> numbers=new ArrayList<>();
		int[] factorial=new int[n+1];
		StringBuilder sb=new StringBuilder();
		int sum=1;
		factorial[0]=1;
		for(int i=1;i<=n;i++)
		{
			sum*=i;
			factorial[i]=sum;
			numbers.add[i];
		}
		k--;
		for(int i=1;i<=n;i++)
		{
			int index=k/factorial[n-i];
			sb.append(String.valueOf(numbers.get(index)));
			numbers.remove(index);
			k-=index*factorial[n-i];
		}
		return String.valueOf(sb);
	}
	{% endhighlight %}