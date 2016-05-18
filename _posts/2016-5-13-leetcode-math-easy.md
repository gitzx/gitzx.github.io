---
date: 2016-5-13 19:03:30+00:00
layout: post
title: Leetcode中数字类题目小结（Easy部分）
thread: 132
categories: algorithm
tags: algorithm

---

这篇小结下Leetcode中Math类Easy部分的题目，目前已有的题目(除去之前已总结的)有：

1. Happy Number

2. Palindrome Number

3. Power of Three

4. Ugly Number

5. Add Digits

6. Reverse Integer

7. Excel Sheet Column Title

8. Factorial Trailing Zeroes

9. Count Primes

10. Rectangle Area

11. Excel Sheet Column Number 

### [Happy Number](https://leetcode.com/problems/happy-number/) ###

Write an algorithm to determine if a number is "happy".

A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.

Example: 19 is a happy number

1^2 + 9^2 = 82

8^2 + 2^2 = 68

6^2 + 8^2 = 100

1^2 + 0^2 + 0^2 = 1

Credits:


### [Palindrome Number](https://leetcode.com/problems/palindrome-number/) ###

Determine whether an integer is a palindrome. Do this without extra space.

click to show spoilers.

Some hints:

Could negative integers be palindromes? (ie, -1)

If you are thinking of converting the integer to string, note the restriction of using extra space.

You could also try reversing an integer. However, if you have solved the problem "Reverse Integer", you know that the reversed integer might overflow. How would you handle such case?

There is a more generic way of solving this problem.

	{% highlight java %}
	public boolean isPalindrome(int x)
	{
		if(x<0||(x!=0&&x%10==0))
		{
			return false;
		}
		int rev=0;
		while(x>rev)
		{
			rev=rev*10+x%10;
			x=x/10;
		}
		return (x==rev||x==rev/10);
	}
	{% endhighlight %}

### [Power of Three](https://leetcode.com/problems/power-of-three/) ###

Given an integer, write a function to determine if it is a power of three.

	{% highlight java %}
	public boolean isPowerOfThree(int n)
	{
		if(n>1)
		{
			while(n%3==0)
			{
				n/=3;
			}
		}
		return n==1;
	}
	{% endhighlight %}

### [Ugly Number](https://leetcode.com/problems/ugly-number/) ###

Write a program to check whether a given number is an ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5. For example, 6, 8 are ugly while 14 is not ugly since it includes another prime factor 7.

Note that 1 is typically treated as an ugly number.


### [Add Digits](https://leetcode.com/problems/add-digits/) ###

Given a non-negative integer num, repeatedly add all its digits until the result has only one digit.

For example:

Given num = 38, the process is like: 3 + 8 = 11, 1 + 1 = 2. Since 2 has only one digit, return it.

Follow up:
Could you do it without any loop/recursion in O(1) runtime?

### [Reverse Integer](https://leetcode.com/problems/reverse-integer/) ###

Reverse digits of an integer.

Example1: x = 123, return 321
Example2: x = -123, return -321

	{% highlight java %}
	public int reverse(int x)
	{
		long rev=0;
		while(x!=0)
		{
			rev=rev*10+x%10;
			x=x/10;
			if(rev>Integer.MAX_VALUE||rev<Integer.MIN_VALUE)
			{
				return 0;
			}
		}
		return (int)rev;
	}
	{% endhighlight %}

### [Excel Sheet Column Title](https://leetcode.com/problems/excel-sheet-column-title/) ###

Given a positive integer, return its corresponding column title as appear in an Excel sheet.

For example:

    1 -> A
    2 -> B
    3 -> C
    ...
    26 -> Z
    27 -> AA
    28 -> AB 

代码如下:

	{% highlight java %}
	public String convertToTitle(int n)
	{
		String ans;
		while(n>0)
		{
			ans=char((n-1)%26+'A')+ans;
			n=(n-1)/26;
		}
		return ans;
	}
	{% endhighlight %}

### [Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) ###

Given an integer n, return the number of trailing zeroes in n!.

Note: Your solution should be in logarithmic time complexity.

### [Count Primes](https://leetcode.com/problems/count-primes/) ###

Description:

Count the number of prime numbers less than a non-negative number, n.

### [Rectangle Area](https://leetcode.com/problems/rectangle-area/) ###

Find the total area covered by two rectilinear rectangles in a 2D plane.

Each rectangle is defined by its bottom left corner and top right corner as shown in the figure.

Rectangle Area

Assume that the total area is never beyond the maximum possible value of int.


### [Excel Sheet Column Number ](https://leetcode.com/problems/excel-sheet-column-number/) ###

Related to question Excel Sheet Column Title

Given a column title as appear in an Excel sheet, return its corresponding column number.

For example:

    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28 

代码如下:

	{% highlight java %}
	public int titleToNumber(String s)
	{
		int result=0;
		for(int i=0;i<s.length();i++)
		{
			result=result*26+(s.charAt(i)-'A'+1);
		}
		return result;
	}
	{% endhighlight %}