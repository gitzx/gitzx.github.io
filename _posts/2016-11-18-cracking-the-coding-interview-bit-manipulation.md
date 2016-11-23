---
date: 2016-11-18 12:05:30+00:00
layout: post
title: 《Cracking the coding interview》中位运算小结
thread: 164
categories: algorithm 
tags: algorithm 

---

这篇小结下《Cracking the coding interview》中的位运算题目。


1. You are given two 32-bit numbers, N and M, and two bit positions, i and j. Write a method to set all bits between i and j in N equal to M (e.g., M becomes a substring of N located at i and starting at j). EXAMPLE: Input: N = 10000000000, M = 10101, i = 2, j = 6 Output: N = 10001010100

2. Given a (decimal - e.g. 3.72) number that is passed in as a string, print the binary representation. If the number can not be represented accurately in binary, print “ERROR”

3. Given an integer, print the next smallest and next largest number that have the same number of 1 bits in their binary representation.

4. Explain what the following code does: ((n & (n-1)) == 0).

5. Write a function to determine the number of bits required to convert integer A to integer B. Input: 31, 14 Output: 2

6. Write a program to swap odd and even bits in an integer with as few instructions as possible (e.g., bit 0 and bit 1 are swapped, bit 2 and bit 3 are swapped, etc).

7. An array A[1…n] contains all the integers from 0 to n except for one number which is missing. In this problem, we cannot access an entire integer in A with a single operation. The elements of A are represented in binary, and the only operation we can use to access them is “fetch the jth bit of A[i]”, which takes constant time. Write code to find the missing integer. Can you do it in O(n) time?


### 位运算基础 ###

1. and与运算(&)

2. or或运算（|）

3. xor异或运算（^）：

	（1）交换律： A^B = B^A
	
	（2）结合律： A^(B^C) = (A^B)^C

	（3）恒等律： A^0 = A

	（4）归零律： A^A = 0
 
	（5）自反： A^B^B = A^0 = A

4. not取反运算（~） ：只有取反运算是单目操作符。

5. shl左移运算（<<）

6. shr右移运算（>>）

常用变换操作：

	去掉最后一位          | (101101->10110)           | x shr 1
	在最后加一个0         | (101101->1011010)         | x shl 1
	在最后加一个1         | (101101->1011011)         | x shl 1+1
	把最后一位变成1       | (101100->101101)          | x or 1
	把最后一位变成0       | (101101->101100)          | x or 1-1
	最后一位取反          | (101101->101100)          | x xor 1
	把右数第k位变成1      | (101001->101101,k=3)      | x or (1 shl (k-1))
	把右数第k位变成0      | (101101->101001,k=3)      | x and not (1 shl (k-1))
	右数第k位取反         | (101001->101101,k=3)      | x xor (1 shl (k-1))
	取末三位              | (1101101->101)            | x and 7
	取末k位               | (1101101->1101,k=5)       | x and (1 shl k-1)
	取右数第k位           | (1101101->1,k=4)          | x shr (k-1) and 1
	把末k位变成1          | (101001->101111,k=4)      | x or (1 shl k-1)
	末k位取反             | (101001->100110,k=4)      | x xor (1 shl k-1)
	把右边连续的1变成0    | (100101111->100100000)    | x and (x+1)
	把右起第一个0变成1    | (100101111->100111111)    | x or (x+1)
	把右边连续的0变成1    | (11011000->11011111)      | x or (x-1)
	取右边连续的1         | (100101111->1111)         | (x xor (x+1)) shr 1
	去掉右起第一个1的左边  | (100101000->1000)         | x and (x xor (x-1))


### 1. 给定两个32位的数，N和M，还有两个指示位的数，i和j。 写程序使得N中第i位到第j位的值与M中的相同 ###

You are given two 32-bit numbers, N and M, and two bit positions, i and j. Write a method to set all bits between i and j in N equal to M (e.g., M becomes a substring of N located at i and starting at j).

EXAMPLE:

Input: N = 10000000000, M = 10101, i = 2, j = 6

Output: N = 10001010100


	{% highlight java %}
	public class UpdateBitsBetween
	{
		public static int updateBits(int n, int m, int i, int j)
		{
			int max = ~0;
			int left = max - ((1 << j) -1);
			int right = ((1 << i) - 1);
			int mask = left | right;
			return (n & mask) | (m << i);
		}
	}
	{% endhighlight %}


### 4. 解答以下代码的作用：((n & (n-1)) == 0) ###


Explain what the following code does: ((n & (n-1)) == 0).


代码的作用是判断一个数是否为2的整数次幂


### 5.计算从整数A变为整数B需要修改的二进制位数 ###

Write a function to determine the number of bits required to convert integer A to integer B.

Input: 31, 14

Output: 2

	{% highlight java %}
	public class BitSwapRequired
	{
		public static int bitSwap(int a, int b)
		{
			int count = 0;
			for(int c = a^b; c != 0; c = c>>1)
			{
				count += c & 1;
			}
			return count;
		}
	}
	{% endhighlight %}


### 6. 交换一个整数二进制表示中的奇数位和偶数位 ###

Write a program to swap odd and even bits in an integer with as few instructions as possible (e.g., bit 0 and bit 1 are swapped, bit 2 and bit 3 are swapped, etc).

	{% highlight java %}
	public class SwapOddEvenBits
	{
		public static int swapOddEven(int x)
		{
			return ( ((x & oxaaaaaaaa) >> 1) | ((x & ox55555555) << 1) );
		}
	}
	{% endhighlight %}



C++版实现可参考： [Cracking the coding interview--问题与解答](http://www.hawstein.com/posts/ctci-solutions-contents.html)

参考：[位运算简介及实用技巧（一）：基础篇](http://www.matrix67.com/blog/archives/263)


